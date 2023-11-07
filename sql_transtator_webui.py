import gradio as gr
import requests



def translate(content, flage='H2S', SQLtype='MySQL'): 
  '''
  S2H == SQL to Hunman SQL语句翻译成自然语言
  H2S == Hunman to SQL 自然语言翻译成SQL语句
  '''

  url = 'http://127.0.0.1:8088/claude/chat'
  headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
  }
  if flage == 'H2S':
    data = {
      'prompt': f"""
                    Translate this natural language query into the SQL language of the {SQLtype} database without changing the case of the entry I gave. Note that you should return the SQL statement without any additional explanation:

                    {content}

                    SQL Query:
                    """
    }

  if flage == 'S2H':
    data = {
      'prompt': f"""
                    Translating the SQL language of this {SQLtype} database into natural language makes it understandable and does not change the case of the entries I have given. Note that you should return to natural language without any additional explanation.

                    {content}

                    SQL Query:
                    """
    }
  else:
     return "入参错误"
    
  response = requests.post(url, headers=headers, json=data) 

  if response.status_code != 200:
     return f"网络错误,http_code：{response.status_code}"
  results = response.json()['claude']

  replacements = {
      '&amp;': '&',
      '&lt;': '<',
      '&gt;': '>',
  }

  for old, new in replacements.items():
      results = results.replace(old, new)

  return results

input_text1 = gr.inputs.Textbox(label="输入:", placeholder="例如：查询学生表中的所有学生姓名")
# 创建选择框
options = ["H2S", "S2H"]
dropdown = gr.inputs.Dropdown(choices=options, label="选择功能（H2S：自然语言转SQL; S2H：SQL转自然语言）", default=options[0])

# 创建回调函数
def process_inputs(input_text1, input_text2, dropdown):
    output_text1 = translate(input_text1, dropdown, input_text2)
    return output_text1

# 创建输出框
input_text2 = gr.inputs.Textbox(label="数据库类型:", placeholder='MYSQL')
output_text1 = gr.outputs.Textbox(label="转换结果：")


# 创建界面


interface = gr.Interface(fn=process_inputs, inputs=[input_text1, input_text2, dropdown], outputs=[output_text1])

# 启动界面
interface.launch()