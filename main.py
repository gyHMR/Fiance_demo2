import schedule
import time
from crawler import crawler
import Const

# 初始化执行次数计数器
execution_count = 0
def job():
    global execution_count  # 使用全局变量来跟踪执行次数
    execution_count += 1  # 每次执行时计数器加1
    # 开始时间
    start_time = time.time()
    print(f"开始第 {execution_count} 次爬取数据...")
    # 调用crawler方法进行数据爬取
    crawler()
    # 结束时间
    end_time = time.time()
    # 计算耗费的时间
    elapsed_time = end_time - start_time
    # 打印耗费的时间
    print(f"第 {execution_count} 次爬取完成，耗费时间：{elapsed_time:.2f}秒，爬取结果保存在dist/{Const.data_path}文件夹下")
    print("五分钟后进行下一次数据爬取","当前时间：", time.strftime("%Y-%m-%d %H:%M:%S"))


print(f"爬虫开始执行，定时爬取({Const.Delay_time}分钟/次)")
job()
# 设置定时任务，每五分钟执行一次job函数
schedule.every(Const.Delay_time).minutes.do(job)




# 无限循环，持续执行定时任务
while True:
    schedule.run_pending()
    time.sleep(2)


# # 测试crawler
# if __name__ == '__main__':
#     job()
