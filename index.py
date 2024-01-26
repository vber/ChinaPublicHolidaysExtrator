import re
import datetime

# 定义年份
year = 2024

# 原始文本
text = """
各省、自治区、直辖市人民政府，国务院各部委、各直属机构：

经国务院批准，现将2024年元旦、春节、清明节、劳动节、端午节、中秋节和国庆节放假调休日期的具体安排通知如下。

一、元旦：1月1日放假，与周末连休。

二、春节：2月10日至17日放假调休，共8天。2月4日（星期日）、2月18日（星期日）上班。鼓励各单位结合带薪年休假等制度落实，安排职工在除夕（2月9日）休息。

三、清明节：4月4日至6日放假调休，共3天。4月7日（星期日）上班。

四、劳动节：5月1日至5日放假调休，共5天。4月28日（星期日）、5月11日（星期六）上班。

五、端午节：6月10日放假，与周末连休。

六、中秋节：9月15日至17日放假调休，共3天。9月14日（星期六）上班。

七、国庆节：10月1日至7日放假调休，共7天。9月29日（星期日）、10月12日（星期六）上班。

节假日期间，各地区、各部门要妥善安排好值班和安全、保卫、疫情防控等工作，遇有重大突发事件，要按规定及时报告并妥善处置，确保人民群众祥和平安度过节日假期。
"""

# text = """
# 各省、自治区、直辖市人民政府，国务院各部委、各直属机构：

# 经国务院批准，现将2023年元旦、春节、清明节、劳动节、端午节、中秋节和国庆节放假调休日期的具体安排通知如下。

# 一、元旦：2022年12月31日至2023年1月2日放假调休，共3天。

# 二、春节：1月21日至27日放假调休，共7天。1月28日（星期六）、1月29日（星期日）上班。

# 三、清明节：4月5日放假，共1天。

# 四、劳动节：4月29日至5月3日放假调休，共5天。4月23日（星期日）、5月6日（星期六）上班。

# 五、端午节：6月22日至24日放假调休，共3天。6月25日（星期日）上班。

# 六、中秋节、国庆节：9月29日至10月6日放假调休，共8天。10月7日（星期六）、10月8日（星期日）上班。

# 节假日期间，各地区、各部门要妥善安排好值班和安全、保卫、疫情防控等工作，遇有重大突发事件，要按规定及时报告并妥善处置，确保人民群众祥和平安度过节日假期。
# """


# 修改extract_holiday_dates函数，对于“月日”格式的日期前面加上年份
def extract_holiday_dates(line, holiday_name, year):
    dates = []

    # 匹配跨年的日期范围
    cross_year_matches = re.findall(r'(\d{4})年(\d+)月(\d+)日至(\d{4})年(\d+)月(\d+)日放假', line)
    for start_year, start_month, start_day, end_year, end_month, end_day in cross_year_matches:
        start_date = datetime.date(int(start_year), int(start_month), int(start_day))
        end_date = datetime.date(int(end_year), int(end_month), int(end_day))
        delta = end_date - start_date
        for i in range(delta.days + 1):
            current_date = start_date + datetime.timedelta(days=i)
            dates.append((current_date.strftime("%Y年%m月%d日"), holiday_name, "假期"))

    # 匹配连续的日期范围
    range_matches = re.findall(r'(\d+)月(\d+)日至(\d+)日放假', line)
    for start_month, start_day, end_day in range_matches:
        start_month, start_day, end_day = int(start_month), int(start_day), int(end_day)
        for day in range(start_day, end_day + 1):
            dates.append((f"{year}年{start_month}月{day}日", holiday_name, "假期"))
    
    # 匹配单独的日期
    single_matches = re.findall(r'(\d+月\d+日)放假', line)
    for date in single_matches:
        if date not in [d[0] for d in dates]:
            dates.append((f"{year}年{date}", holiday_name, "假期"))

    # 匹配“星期”的字符串，提取非假期日期
    non_holiday_matches = re.findall(r'(\d+月\d+日)（星期[^）]+）', line)
    for date in non_holiday_matches:
        if date not in [d[0] for d in dates]:
            dates.append((f"{year}年{date}", f"{holiday_name}调休", "非假期"))

    return dates

# 提取放假信息的原始文本
holiday_info = re.findall(r'^[一二三四五六七]、.*?。$', text, re.M)

# 提取假期名称
holiday_names = [re.search(r'^[一二三四五六七]、(.*?)：', line).group(1) for line in holiday_info]

# 遍历放假信息并提取日期
all_dates = []
for line, holiday_name in zip(holiday_info, holiday_names):
    dates = extract_holiday_dates(line, holiday_name, year)
    all_dates.extend(dates)

# 输出结果
for date, holiday_name, label in all_dates:
    print(f"{date} {holiday_name} {label}")
