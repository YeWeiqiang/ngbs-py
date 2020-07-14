from selenium import webdriver
import time

LOGIN_URL = "http://xgfx.bnuz.edu.cn/xsdtfw/sys/emapfunauth/pages/funauth-login.do?service=%2Fxsdtfw%2Fsys%2Femapfunauth%2Fpages%2Femap-userinfo.do#/"



def login(wd, stu_no, stu_password):
    wd.get(LOGIN_URL)
    time.sleep(1)

    wd.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div/div[3]/div/div[1]/div/div[1]/div/input').send_keys(
        stu_no)
    wd.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div/div[3]/div/div[2]/div/div/div/input').send_keys(
        stu_password)
    wd.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div/div[3]/div/div[3]/div/button').click( )
    time.sleep(1)

    try:
        name = wd.find_element_by_xpath('/html/body/main/header/div[1]/div[1]').text
        print(name)
        # 进入疫情自查上报
        wd.find_element_by_xpath('/html/body/main/article/section[1]/div/div/div/div[2]/div/div/div[2]').click( )
        time.sleep(1)
        windows = wd.window_handles  # 获取该会话所有的句柄
        wd.switch_to.window(windows[-1])  # 跳转到最新的句柄
        time.sleep(5)

        return True

    except Exception as e:
        # 登录失败
        print(e)
        return False
        # errMsg = wd.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div/div[2]').text


def reportEpidemic(wd):
    time.sleep(3)
    try:
        # 体温
        wd.find_element_by_xpath(
            '/html/body/main/article/section/div[2]/div[2]/div/div[2]/div[2]/div[2]/div/div/input').send_keys(
            '36.8')
        # 今日本人是否身体不适（包括发烧、...
        wd.find_element_by_xpath(
            '/html/body/main/article/section/div[2]/div[2]/div/div[2]/div[2]/div[6]/div/div/div[2]/div').click( )
        time.sleep(0.3)
        wd.find_element_by_xpath('/html/body/div[24]/div/div/div/div[2]/div/div[3]').click( )
        # 本人或家属是否有疫区人员接触史
        wd.find_element_by_xpath(
            '/html/body/main/article/section/div[2]/div[2]/div/div[2]/div[2]/div[8]/div/div/div[2]/div').click( )
        time.sleep(0.3)
        wd.find_element_by_xpath('/html/body/div[26]/div/div/div/div[2]/div/div[3]').click( )
        # 本人或家属是否与疑似或确诊患者接触过
        wd.find_element_by_xpath(
            '/html/body/main/article/section/div[2]/div[2]/div/div[2]/div[2]/div[10]/div/div/div[2]/div').click( )
        time.sleep(0.3)
        wd.find_element_by_xpath('/html/body/div[28]/div/div/div/div[2]/div/div[3]').click( )
        # 本人或家属是否为疑似病例或有确诊病例
        wd.find_element_by_xpath(
            '/html/body/main/article/section/div[2]/div[2]/div/div[2]/div[2]/div[12]/div/div/div[2]/div').click( )
        time.sleep(0.3)
        wd.find_element_by_xpath('/html/body/div[30]/div/div/div/div[2]/div/div[3]').click( )
        # 本人或家属是否被居家隔离或医学隔离
        wd.find_element_by_xpath(
            '/html/body/main/article/section/div[2]/div[2]/div/div[2]/div[2]/div[14]/div/div/div[2]/div').click( )
        time.sleep(0.3)
        wd.find_element_by_xpath('/html/body/div[32]/div/div/div/div[2]/div/div[3]').click( )
        # 保存
        wd.find_element_by_xpath('/html/body/main/article/footer/a[1]').click( )

        time.sleep(2)
        respone = getInfo(wd)
        respone["report"] = "true"
        return respone


    except Exception as e:
        # 已完成上报
        print("已完成上报")
        time.sleep(2)
        return getInfo(wd)


def getInfo(wd):
    try:
        # 点击自定义列
        wd.find_element_by_xpath('/html/body/main/article/section/div/div[2]/span').click( )
        # 先全选，再取消全选
        wd.find_element_by_xpath('/html/body/div[11]/div[2]/div[1]/div/div[1]/div[2]/div[1]/div/label/input').click( )
        wd.find_element_by_xpath('/html/body/div[11]/div[2]/div[1]/div/div[1]/div[2]/div[1]/div/label/input').click( )
        # 学号
        wd.find_element_by_name('XH').click( )
        # 姓名
        wd.find_element_by_name('XM').click( )
        # 性别
        wd.find_element_by_name('XBDM').click( )
        # 填报日期
        wd.find_element_by_name('TBSJ').click( )
        # 班级
        wd.find_element_by_name('BJDM').click( )
        # 保存
        wd.find_element_by_xpath('/html/body/div[11]/div[2]/div[2]/button[2]').click( )
        # 获取表格的第一行数据
        tbody = wd.find_element_by_xpath(
            '/html/body/main/article/section/div/div[3]/div[2]/div/div[4]/div[2]/div/table/tbody/tr[1]').text
        tbody = tbody.split(" ")
        # ['编辑', '|', '查看', '1701040120', '叶威强', '男', '2020-07-13', '17软件01']
        # 删除前三个无用字段
        del (tbody[0])
        del (tbody[0])
        del (tbody[0])
        # ['1701040120', '叶威强', '男', '2020-07-13', '17软件01']
        print(tbody)
        data = {}
        data["XH"] = tbody[0]
        data["XM"] = tbody[1]
        data["XBDM"] = 1 if tbody[2] == '男' else 0
        data["TBSJ"] = tbody[3]
        data["BJ"] = tbody[4]
        print(data)
        respon = {"code": 200, "data": data}
        print(respon)
        return respon

    except Exception as e:
        print(e)
        return {"code": 404}


def run(stu_no, stu_password):
    try:
        option = webdriver.ChromeOptions( )
        option.add_argument('window-size=1920x3000')  # 指定浏览器分辨率
        option.add_argument('--headless')
        option.add_argument('--disable-gpu')
        option.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
        wd = webdriver.Chrome(chrome_options=option)
        # 全屏
        wd.maximize_window( )
        doLogin = login(wd, stu_no, stu_password)

        if not doLogin:
            return {"code": 401}

        time.sleep(3)
        response = reportEpidemic(wd)
        # 关闭所有窗口
        wd.quit( )
        return response

    except Exception as e:
        # 关闭所有窗口
        wd.quit( )
        return {"code": 404}



if __name__ == "__main__":

    print(run("", ""))
