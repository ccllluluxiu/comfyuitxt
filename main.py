from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
import astrbot.api.message_components as Comp
from astrbot.api import logger
import json
import random
import time
import requests

@register("comfyuitxtimg", "cc", "一个简单的 comfyui 插件", "1.3.1")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        # ComfyUI服务器地址配置
        self.comfyui_api_url = "http://38.55.205.201:12347/"  # 默认本地地址，可根据实际情况修改
        
    # 注册指令的装饰器。指令名为 comfyui。注册成功后，发送 `/comfyuitxt` 就会触发这个指令
    # @filter.command("comfyuitxt")
    @filter.command_group("comfyuitxt")
    def comfyuitxt():
        pass
    @comfyuitxt.group("calc") # 请注意，这里是 group，而不是 command_group
    def calc():
        pass
    @calc.command("sd15")
    async def sd15(self, event: AstrMessageEvent,positive: str):
        """这是一个 txt-img 指令"""
        # user_name = event.get_sender_name()
        # message_str = event.message_str
        # message_str = message_str.split("omfyuitxt15")
        # logger.info(message_str)
        # positive = message_str[1]
        logger.info(positive)
        #构造json 工作流
        # prompt = json.load(open('/AstrBot/data/plugins/comfyuitxt/sd15.json', encoding='utf-8'))
        # prompt["3"]["inputs"]["text"] = "1girl, blue eyes, blue hair, blue dress"
        prompt = json.load(open('/AstrBot/data/plugins/comfyuitxt/sd15a.json', encoding='utf-8'))
        prompt["12"]["inputs"]["positive"] += positive
        prompt["4"]["inputs"]["seed"] = random.randint(1, 9999999)
        url = self.comfyui_api_url
        p = {
            "prompt": prompt,
            "client_id": "ccdd"
        }
        #发生绘图请求
        r = requests.post(url+"prompt", json=p)
        #获取绘图ID
        prompt_id = r.json()["prompt_id"]

        response = ""
        f = 5
        #请求绘图结果
        while f:
            time.sleep(5)
            try:
                response = requests.get(url+"history/"+prompt_id)
                # 如果获取到了有效的历史记录，则提前退出循环
                if response.status_code == 200 and response.json():
                    break
            except Exception as e:
                logger.info(f"请求出错: {e}")
            f -= 1

        if response:
            # print(response.json())
            img_name=response.json()[prompt_id]['outputs']['10']['images'][0]['filename']
            # print(img_name)
            img_url = url+"view?filename="+img_name+"&type=output"
            # print(img_url)
            chain = [
                    Comp.Plain("喵喵15"),
                    Comp.At(qq=event.get_sender_id()), # At 消息发送者
                    Comp.Image.fromURL(img_url)  # 从 URL 发送图片
                ]
            yield event.chain_result(chain)

        else:
             yield event.plain_result("失败哩，嘻嘻")
    @calc.command("xlil")
    async def xlil(self, event: AstrMessageEvent,positive: str):
        """这是一个 txt-img 指令"""
        # user_name = event.get_sender_name()
        # message_str = event.message_str
        # message_str = message_str.split("omfyuitxtil")
        # logger.info(message_str)
        # positive = message_str[1]
        positive = (positive)
        logger.info(positive)
        #构造json 工作流
        # prompt = json.load(open('/AstrBot/data/plugins/comfyuitxt/sd15.json', encoding='utf-8'))
        # prompt["3"]["inputs"]["text"] = "1girl, blue eyes, blue hair, blue dress"
        prompt = json.load(open('/AstrBot/data/plugins/comfyuitxt/xlli00.json.json', encoding='utf-8'))
        prompt["8"]["inputs"]["text"] = positive
        prompt["2"]["inputs"]["seed"] = random.randint(1, 9999999)
        url = self.comfyui_api_url
        p = {
            "prompt": prompt,
            "client_id": "ccdd"
        }
        #发生绘图请求
        r = requests.post(url+"prompt", json=p)
        #获取绘图ID
        prompt_id = r.json()["prompt_id"]

        response = ""
        f = 4
        #请求绘图结果
        while f:
            time.sleep(20)
            try:
                response = requests.get(url+"history/"+prompt_id)
                # 如果获取到了有效的历史记录，则提前退出循环
                if response.status_code == 200 and response.json():
                    break
            except Exception as e:
                logger.info(f"请求出错: {e}")
            f -= 1

        if response:
            # print(response.json())
            img_name=response.json()[prompt_id]["outputs"]["4"]["images"][0]["filename"]
            # print(img_name)
            img_url = url+"view?filename="+img_name+"&type=output"
            # print(img_url)
            chain = [
                    Comp.Plain("喵喵il"),
                    Comp.At(qq=event.get_sender_id()), # At 消息发送者
                    Comp.Image.fromURL(img_url)  # 从 URL 发送图片
                ]
            yield event.chain_result(chain)

        else:
             yield event.plain_result("失败哩，嘻嘻")

                


        