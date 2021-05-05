import pandas as pd
import json as json
import urllib.request as request
import requests
import numpy as np

from IPython.display import display, Javascript, HTML
import random

import plotly.graph_objects as go
from plotly.subplots import make_subplots

def get_dataframe_from_fedcat_api(url, column_list=''):
    """
    Call the API URL passed and return a dataframe with the results.
    """
    # Read URL
    with request.urlopen(url) as response:
        if response.getcode() == 200:
            source = response.read()
            data = json.loads(source)

            # FedCat api's return rows within "source" attribute
            rows = data["source"]

            # Creates DataFrame.
            if (column_list == ''):
                # if the coumn list is not specified,
                # derive the data frame column sepecification based on the filters passed to the API
                # (Note, FedCat refers to filters as the data attributes being requested)
                filter_parameter_name='&filters'
                filter_start_index = url.find(filter_parameter_name)
                if (filter_start_index>-1) :
                    filter_end_index = url.find('&',filter_start_index+1)
                    filters_string = url[filter_start_index+len(filter_parameter_name)+1:filter_end_index==-1 and len(url) or filter_end_index]
                    keys = filters_string.split(",")
                else:
                    # if the coumn list and filters were not specified,
                    # derive the data frame column sepecification based on the keys returned.
                    keys = data["source"][0].keys()
                    low_number_keys = len(keys)
                    high_number_keys = len(keys)
                    for row in rows:
                        if (len(row)<low_number_keys): low_number_keys = len(row)
                        if (len(row)>high_number_keys): 
                            keys = row.keys()
                            high_number_keys = len(row)                
                df = pd.DataFrame(data["source"],columns=keys)  
            else:
                df = pd.DataFrame(data["source"],columns=column_list) 
            return df
        else:
            print('An error occurred while attempting to retrieve data from the API.  Response code: ', response.getcode())
            return None
 

def build_hierarchical_dataframe(df, levels, value_column, color_columns=None):
    """
    Build a hierarchy of levels for Sunburst or Treemap charts.

    Levels are given starting from the bottom to the top of the hierarchy, 
    ie the last level corresponds to the root.
    """
    df_all_trees = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
    for i, level in enumerate(levels):
        df_tree = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
        dfg = df.groupby(levels[i:]).sum(numerical_only=True)
        dfg = dfg.reset_index()
        df_tree['id'] = dfg[level].copy()
        if i < len(levels) - 1:
            df_tree['parent'] = dfg[levels[i+1]].copy()
        else:
            df_tree['parent'] = 'total'
        df_tree['value'] = dfg[value_column]
        df_tree['color'] = dfg[color_columns[0]]
        df_all_trees = df_all_trees.append(df_tree, ignore_index=True)
    total = pd.Series(dict(id='total', parent='', 
                              value=df[value_column].sum(),
                              color=df[value_column].sum()))
    df_all_trees = df_all_trees.append(total, ignore_index=True)
    return df_all_trees

def build_sunburst(df, levels):
    """
    Build side by side Sunburst charts, one fully expanded and the other with
    a maximum depth of 2.

    Levels are given starting from the bottom to the top of the hierarchy, 
    ie the last level corresponds to the root.
    """
    color_columns = ['count']
    value_column = 'count'
    df_all_trees = build_hierarchical_dataframe(df, levels, value_column, color_columns)
    
    fig = make_subplots(1, 2, specs=[[{"type": "domain"}, {"type": "domain"}]],)
    fig.add_trace(go.Sunburst(
      labels=df_all_trees['id'],
      parents=df_all_trees['parent'],
      values=df_all_trees['value'],
      branchvalues='total',
      hovertemplate='<b>%{label} </b> <br> Offering count: %{value}',
      name=''
      ), 1, 1)

    fig.add_trace(go.Sunburst(
      labels=df_all_trees['id'],
      parents=df_all_trees['parent'],
      values=df_all_trees['value'],
      branchvalues='total',
      hovertemplate='<b>%{label} </b> <br> Offering count: %{value}',
      maxdepth=2,
      name=''
      ), 1, 2)
    
    fig.update_layout(margin=dict(t=10, b=10, r=10, l=10))
    fig.show()   

def recur_dictify(frame):
    if len(frame.columns) == 1:
        if frame.values.size == 1: return frame.values[0][0]
        return frame.values.squeeze()
    grouped = frame.groupby(frame.columns[0])
    d = {k: recur_dictify(g.iloc[:,1:]) for k,g in grouped}
    return d

def dict_to_json(d, level, json_str):
    tab = "  " * level   
    separator = "" 
    for k, v in d.items():
        if isinstance(v, dict):
            json_str += (tab+separator+"{\n")
            json_str += (tab+"    \"name\": \""+str(k)+"\",\n")
            json_str += (tab+"    \"children\": [\n")

            json_str = dict_to_json(v, level+1, json_str)

            json_str += (tab+"    ]\n")
            json_str += (tab+"}\n")
            separator = ","
        else:
            d_len = len(d)
            key_offset = list(d).index(k)
            sep1 = ","
            if (d_len == (key_offset+1)): sep1 = ""
            json_str += (tab+"  {\n")
            json_str += (tab+"    \"name\": \""+str(k)+"\",\n")
            json_str += (tab+"    \"children\": [\n")
            sep2=""
            arr_cnt = 1
            if isinstance(v, np.ndarray):
                for vs in v:
                    if arr_cnt == len(v):
                        sep2=""
                    else:
                        sep2=","
                    arr_cnt = arr_cnt + 1
                    json_str += (tab+"         { \"name\": \""+str(vs)+"\" }"+sep2+"\n")
            else:
                if (str(v)!='(null)'):
                    json_str += (tab+"         { \"name\": \""+str(v)+"\" }\n")
            json_str += (tab+"    ]\n")
            #print("{0} : {1}".format(k, v)) 
            json_str += (tab+"  }"+sep1+"\n") 

    return json_str

def draw_tree(jsonFileName, width=600, height=400):
    #print("draw_tree", jsonFileName, width, height)
    display(Javascript("""
        (function(element){
            require(['trees'], function(trees) {
                trees(element.get(0), %s, %d, %d);
            });
        })(element);
    """ % (jsonFileName, width, height)))        

def build_tree(df, levels, width=960, height=700, json_file_name="data/my-tree.json"):
    ut_tree_df = df[levels].drop_duplicates() 
    #ut_tree_df["utl10"]="GBS"
    #cols = ut_tree_df.columns.tolist()
    #cols = cols[-1:] + cols[:-1]
    #ut_tree_df = ut_tree_df[cols]
    ut_tree_dict = recur_dictify(ut_tree_df) 
    ut_tree_json = dict_to_json(ut_tree_dict,0, "")
    f = open(json_file_name, "w")
    f.write(ut_tree_json)
    f.close()
    draw_tree(json.dumps({"jsonFile":json_file_name}),width, height)   


def draw_tree_from_json_file(json_file_name, width=600, height=400):
    draw_tree(json.dumps({"jsonFile":json_file_name}),width, height)   


def flatten_self_referencing_df(parent_child_df, level_col_nm, id_col_nm, desc_col_nm, parent_col_nm):
    """
    Take a dataframe with self-referencing columns and return a dataframe with a flattened hierarchy as the results.
    """
    # identify terminal items
    last = parent_child_df[~parent_child_df[id_col_nm].isin(pd.to_numeric(parent_child_df[parent_col_nm],
                                                            errors='coerce'))]
    # find max hierarchy level
    mx = parent_child_df[level_col_nm].max()
    
    # build a list for any terminal items with all of its parents
    data = []
    for _, row in last.iterrows():
        # initialize row
        hrow= {'lvl'+str(i+1)+ext: '' for i in range(mx) for ext in ['', 'desc']}
        # populate lvli and lvlidesc for the item and its parents
        for lvl in range(row[level_col_nm], 0, -1):
            hrow['lvl'+str(lvl)] = row[id_col_nm]
            hrow['lvl'+str(lvl) + 'desc'] = row[desc_col_nm]
            # process parent until top level
            try:
                row = parent_child_df[parent_child_df[id_col_nm]==int(row[parent_col_nm])].iloc[0]
            except:
                break
        data.append(hrow)

     # build the resulting dataframe
    flat_df = pd.DataFrame(data)
    return flat_df   

def executeSql(host, auth_header, sql, sql_limit=1000):
    sql_command = {
      "commands" : sql,
      "limit" : sql_limit,
      "separator" : ";",
      "stop_on_error" : "yes"
    }
    service = "/sql_jobs"
    r = requests.post(host + service, headers=auth_header, json=sql_command)
    if r.status_code == 201:
        return r.json()['id']
    else:
        print("Something went wrong with the call.  Status code = "+r.status_code)
        return None
    
def getResults(host, auth_header, jobid):
    r = requests.get(host + "/sql_jobs/" + jobid, headers=auth_header)
    if r.status_code != 200:
        print("Something went wrong with the call.  Status cd="+str(r.status_code))
        return None
    results = r.json()['results']
    
    if (len(results)==0):
        print("Results are empty or already retrieved.")
        return None    
    
    if('error' in results[0]):
        print("ERROR - ", results[0]['error'])
        return None
    
    columns = results[0]['columns']
    rows = results[0]['rows']
    df = pd.DataFrame(data=rows,columns=columns)
    cols = df.columns
    df[cols] = df[cols].apply(pd.to_numeric, errors='ignore')
    return df
    
def print_methods(object, spacing=20):
  methodList = []
  for method_name in dir(object):
    try:
        if callable(getattr(object, method_name)):
            methodList.append(str(method_name))
    except:
        methodList.append(str(method_name))
  processFunc = (lambda s: ' '.join(s.split())) or (lambda s: s)
  for method in methodList:
    try:
        print(str(method.ljust(spacing)) + ' ' +
              processFunc(str(getattr(object, method).__doc__)[0:90]))
    except:
        print(method.ljust(spacing) + ' ' + ' getattr() failed')    

def hide_toggle(for_next=False):
    this_cell = """$('div.cell.code_cell.rendered.selected')"""
    next_cell = this_cell + '.next()'

    toggle_text = 'Toggle show/hide'  # text shown on toggle link
    target_cell = this_cell  # target cell to control with toggle
    js_hide_current = ''  # bit of JS to permanently hide code in current cell (only when toggling next cell)

    if for_next:
        target_cell = next_cell
        toggle_text += ' next cell'
        js_hide_current = this_cell + '.find("div.input").hide();'

    js_f_name = 'code_toggle_{}'.format(str(random.randint(1,2**64)))

    html = """
        <script>
            function {f_name}() {{
                {cell_selector}.find('div.input').toggle();
            }}

            {js_hide_current}
        </script>

        <a href="javascript:{f_name}()">{toggle_text}</a>
    """.format(
        f_name=js_f_name,
        cell_selector=target_cell,
        js_hide_current=js_hide_current, 
        toggle_text=toggle_text
    )

    return HTML(html)