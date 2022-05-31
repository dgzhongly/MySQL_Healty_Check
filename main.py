from sys import exit
from argparse import ArgumentParser
from getpass import getpass
import analyze
import report
import osconnection
import dbconnection
import workload


version = 'MySQL Health Checker V1.3.3 Develop by Rex-zly'


def argparse():
    parser = ArgumentParser()
    parser.add_argument(
        "-u",
        "--user",
        type=str,
        default="root",
        help="数据库 user"
    )
    parser.add_argument(
        "-p",
        "--password",
        default=None,
        help="数据库 password",
    )
    parser.add_argument(
        "-H",
        "--host",
        help="主机地址，当该参数被指定时，socket参数失效，该参数自动作为报告的名字"
    )
    parser.add_argument(
        "-P",
        "--port",
        help="数据库 port",
        default="3306"
    )
    parser.add_argument(
        "-S",
        "--socket",
        help="socket 文件路径",
        default="/tmp/mysql.sock"
    )
    parser.add_argument(
        "--version",
        help="显示版本信息",
        default=False,
        action='store_true'
    )
    parser.add_argument(
        "--sql",
        help="输出用于巡检的SQL语句，并退出",
        default=False,
        action='store_true'
    )
    parser.add_argument(
        "-o",
        "--output",
        help="报告保存的路径",
        default=None
    )
    parser.add_argument(
        "-n",
        "--name",
        help="指定报告的名字，自动添加.docx后缀。默认使用 ip_port_date.docx 作为报告名。",
        default=None
    )
    parser.add_argument(
        "--skip_tables",
        help="跳过查询information_schema.tables。在一些特定场景下，该表因数量过大而导致需要大量查询时间。跳过此表将导致缺失与该表相关的信息",
        default=False,
        action='store_true'
    )
    parser.add_argument(
        "--workload",
        help="开启负载监控",
        default=False,
        action='store_true'
    )
    parser.add_argument(
        "-i",
        "--interval",
        help="负载监控数据采集间隔，单位秒，默认为3秒一次",
        type=int,
        default=3,
    )
    parser.add_argument(
        "-t",
        "--time",
        help="负载监控数据采集时间，单位秒，默认为600秒",
        type=int,
        default=600,
    )

    return parser.parse_args()


args = argparse()

if args.version:
    print(version)
    exit(0)

if args.sql:
    from sql80 import sql
    for i in sql:
        print()
        print(i[0])
        s = i[1].split()
        for j in s:
            print(j, end=' ')
        print(';')
    exit(0)

if not args.password:
    args.password = getpass()


if __name__ == '__main__':
    dbconnection.get_db_info()
    osconnection.get_os_info()
    workload_info = None
    if args.workload:
        workload_info = workload.get_workload_info()
    analyze.analyze()
    report.make_report(workload_info)
