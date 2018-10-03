import math
import numpy as np



def read_file_num(filename):
    file = open(filename, "r")
    lines = file.readlines()
    arr = []
    for line in lines:
        arr.append(float(line))
    return arr



def read_file_str(filename):
    file = open(filename, "r")
    lines = file.readlines()
    arr = []
    for line in lines:
        arr.append(line)
    return arr[0]



def write_file_avg_time(arr, file_name):
    with open(file_name, "w") as file:
        file.write("%.3f" % (arr[0]))



def write_file_departure_table(arr, file_name):
    with open(file_name, "w") as file:
        for i in range(len(arr)):
            file.write("%.3f" % (arr[i][0]))
            file.write("\t")
            file.write("%.3f" % (arr[i][1]))



def random_num_arrive(lmd):
    np.random.seed(1)
    return (-1 * math.log(1-np.random.rand(1))/lmd)



def random_num_service(mu):
    np.random.seed(1)
    sk = 0
    for i in range(3):
        sk += (-1 * math.log(1-np.random.rand(1))/mu)
    return sk



def simulation(mode, arrival, service, m, setup_time, delayedoff_time, time_end):
    if(mode == "trace"):
        num_of_unmarked_job = 0
        time_line = []
        list_of_idle_service = []
        queue = []
        real_departure = []
        server_state = [[],[],[]]
        for i in range(1, m+1):
            list_of_idle_service.append(i)
            server_state[0].append(i)
            server_state[1].append("OFF")
            server_state[2].append(-1)
        # 上面的二维数组记录的是每个服务器的状态，第一个list放编号，第二个list放状态，第三个list放在什么时候启动

        time_point = 0
        for i in range(len(arrival)):
            event_arrival = []
            event_arrival.append(arrival[i])
            event_arrival.append("job_arrive")
            event_arrival.append("unmarked")
            event_arrival.append(i+1)
            time_line.append(event_arrival)
        # 首先，把所有job的到达时间和离开时间都放在时间线里面。

    if(mode == "random"):
        num_of_unmarked_job = 0
        time_line = []
        list_of_idle_service = []
        queue = []
        real_departure = []
        server_state = [[],[],[]]
        for i in range(1, m+1):
            list_of_idle_service.append(i)
            server_state[0].append(i)
            server_state[1].append("OFF")
            server_state[2].append(-1)
        # 上面的二维数组记录的是每个服务器的状态，第一个list放编号，第二个list放状态，第三个list放在什么时候启动

        time_point = 0

        arrival = [10]
        service = [1]


        arrival = [random_num_arrive(lmd)]
        service = [random_num_service(mu)]
        for i in range(len(arrival)):
            event_arrival = []
            event_arrival.append(arrival[i])
            event_arrival.append("job_arrive")
            event_arrival.append("unmarked")
            event_arrival.append(i+1)
            time_line.append(event_arrival)
        # 首先，把所有job的到达时间和离开时间都放在时间线里面。

    while(time_point <= (len(time_line)-1)):
        if(time_line[time_point][1] == "job_arrive"):
            if(mode == "random"):
                # if((time_line[time_point][0]+10) < time_end):
                #     arrival.append(time_line[time_point][0]+10)
                #     event_arrival = []
                #     event_arrival.append(time_line[time_point][0]+10)
                #     event_arrival.append("job_arrive")
                #     event_arrival.append("unmarked")
                #     event_arrival.append(time_line[time_point][-1]+1)
                #     time_line.append(event_arrival)
                #     time_line = sorted(time_line, key=lambda x: x[0])
                #     service.append(service[-1]+1)
                next_arrive_time = time_line[time_point][0]+random_num_arrive(lmd)
                next_service_time = random_num_service(mu)
                if(next_arrive_time < time_end):
                    arrival.append(next_arrive_time)
                    event_arrival = []
                    event_arrival.append(next_arrive_time)
                    event_arrival.append("job_arrive")
                    event_arrival.append("unmarked")
                    event_arrival.append(time_line[time_point][-1]+1)
                    time_line.append(event_arrival)
                    time_line = sorted(time_line, key=lambda x: x[0])
                    service.append(next_service_time)
            # 如果有新的job进入系统
            queue.append(arrival.index(time_line[time_point][0]) + 1)
            # 第几个job到达了，就在数组queue中添加第几个job的编号
            if(time_line[time_point][2] == "unmarked"):
                num_of_unmarked_job += 1
                if(len(list_of_idle_service) > 0):
                    time_line[time_point][2] = "marked"
                    num_of_unmarked_job -= 1
                    # 如果有剩余的闲置服务器，把当前没标记的任务变为已标记，并把没被标记的任务的数量减少一个
                    flag = 0
                    # 开关，判断进入哪个条件
                    index_record = []
                    off_time_record = []
                    for k in range(len(server_state[0])):
                        if(server_state[1][k] == "WAITING"):
                            # 有一种情况：当有服务器还在delayed-off阶段时（还没关机，有任何新的任务到来可以直接处理），如果有新的任务到来，就直接处理新的任务。
                            flag = 1
                            index_record.append(k)
                            off_time_record.append(server_state[2][k])
                    if(flag == 1):
                        max_off_time_pos = off_time_record.index(max(off_time_record))
                        max_off_time_pos = index_record[max_off_time_pos]
                        # 如果有多个服务器都在等待关闭，找出最晚关闭的那个服务器进行服务
                        server_state[1][max_off_time_pos] = "BUSY"
                        server_state[2][max_off_time_pos] = -1
                        # 把服务器的状态变为忙碌
                        event_direct_service = []
                        event_direct_service.append(time_line[time_point][0] + service[queue[0]-1])
                        event_direct_service.append("job_finish")
                        event_direct_service.append(server_state[0][max_off_time_pos])
                        event_direct_service.append(queue[0])
                        time_line.append(event_direct_service)
                        time_line = sorted(time_line, key=lambda x: x[0])
                        # 把将来完成这个job的时间信息加到时间线中
                        departure_info = []
                        departure_info.append(time_line[time_point][-1])
                        departure_info.append(time_line[time_point][0] + service[queue[0]-1])
                        real_departure.append(departure_info)
                        # 把这个job的离开时间记录到离开表里面
                        for i in range(time_point, len(time_line)):
                            if (time_line[i][1] == "waiting_off" and time_line[i][2] == server_state[0][max_off_time_pos]):
                                del time_line[i]
                                # 既然服务器原有的delayed-off状态被打断，那么服务器就要删除倒计时器（在时间线中删除这个时间点），等到整个系统中再次没有任务时再启动计时器。
                                break
                        list_of_idle_service.remove(server_state[0][max_off_time_pos])
                        # 这个服务器现在是忙碌状态，所以在空闲服务器列表中将这个服务器拿掉
                        del queue[0]
                        # 把队列中的第一个任务拿掉，因为此时它已经被交予server处理
                        time_point += 1
                        # 移动到下一个时间点

                    else:
                        # 如果不是上面的特殊情况，就来到了一般情况，每个job到来的时候闲置的服务器都是关闭的，需要先让服务器启动
                        server_state[1][list_of_idle_service[0] - 1] = "SETUP"
                        server_state[2][list_of_idle_service[0] - 1] = time_line[time_point][0] + setup_time
                        # 把对应服务器的状态更改为启动，并且在第三个对应数组中来添加服务器的启动完成时间
                        event_setup_and_mark = []
                        event_setup_and_mark.append(time_line[time_point][0] + setup_time)
                        event_setup_and_mark.append("setup_until")
                        event_setup_and_mark.append(list_of_idle_service[0])
                        event_setup_and_mark.append(time_line[time_point][-1])
                        time_line.append(event_setup_and_mark)
                        time_line = sorted(time_line, key=lambda x: x[0])
                        # 把服务器启动这个事件（时间点记录到启动完成）添加到时间线中
                        del list_of_idle_service[0]
                        # 这个服务器现在是启动状态，所以在空闲服务器列表中将这个服务器拿掉
                        time_point += 1
                        # 移动到下一个时间点
                else:
                    # 如果当前没有闲置的服务器来标记新来的job，那么就暂时不标记，直接跳过
                    time_point += 1
                    # 移动到下一个时间点

        elif(time_line[time_point][1] == "setup_until"):
            # 进入这个条件代表服务器开始服务，如果服务完成，则先还回服务器，找时间线
            server_state[1][time_line[time_point][-2] - 1] = "BUSY"
            server_state[2][time_line[time_point][-2] - 1] = -1
            # 既然时间来到了某个服务器的启动完成时间，服务器就开始处理job，把服务器的状态变为忙碌
            event_service_and_return = []
            print(queue)
            event_service_and_return.append(time_line[time_point][0] + service[queue[0]-1])
            event_service_and_return.append("job_finish")
            event_service_and_return.append(time_line[time_point][-2])
            event_service_and_return.append(queue[0])
            time_line.append(event_service_and_return)
            time_line = sorted(time_line, key=lambda x: x[0])
            # 把将来完成这个job的时间信息加到时间线中
            departure_info = []
            departure_info.append(time_line[time_point][-1])
            departure_info.append(time_line[time_point][0] + service[queue[0]-1])
            real_departure.append(departure_info)
            # 把这个job的离开时间记录到离开表里面
            del queue[0]
            # 把队列中的第一个任务拿掉，以为此时它已经被交予server处理
            time_point += 1
            # 移动到下一个时间点

        elif(time_line[time_point][1] == "job_finish"):
            list_of_idle_service.append(time_line[time_point][-2])
            list_of_idle_service = list(set(list_of_idle_service))
            # 如果走到job-finish时间节点，说明任务已经处理完成，还回已经占用的服务器
            server_state[1][time_line[time_point][-2] - 1] = "FINDING"
            server_state[2][time_line[time_point][-2] - 1] = -1
            # 改变服务器的状态为：查找（因为服务器要看队列里面有没有在排队等待处理的任务）
            if(len(queue) > 0):
                # 如果服务器看到队列里面有在排队等待处理的任务，那么就直接处理这个任务）
                server_state[1][time_line[time_point][-2] - 1] = "BUSY"
                server_state[2][time_line[time_point][-2] - 1] = -1
                # 服务器开始处理job，把服务器的状态变为忙碌
                event_service_head_of_queue = []
                event_service_head_of_queue.append(time_line[time_point][0] + service[queue[0]-1])
                event_service_head_of_queue.append("job_finish")
                event_service_head_of_queue.append(time_line[time_point][-2])
                event_service_head_of_queue.append(queue[0])
                time_line.append(event_service_head_of_queue)
                time_line = sorted(time_line, key=lambda x: x[0])
                # 把将来完成这个job的时间信息加到时间线中
                departure_info = []
                departure_info.append(queue[0])
                departure_info.append(time_line[time_point][0] + service[queue[0]-1])
                real_departure.append(departure_info)
                # 把这个job的离开时间记录到离开表里面
                list_of_idle_service.remove(time_line[time_point][-2])
                # 这个服务器现在是忙碌状态，所以在空闲服务器列表中将这个服务器拿掉
                del queue[0]
                if(num_of_unmarked_job > 0):
                    num_of_unmarked_job -= 1
                    # 当处理完成一个任务之后，如果队列中还存在没有被标记的任务，那么就把这个任务标记
                else:
                    num_of_active_server = 0
                    for ele in server_state[1]:
                        if(ele != "OFF"):
                            num_of_active_server += 1
                    if((len(queue)+1) < num_of_active_server):
                        # 如果队列中剩下的任务（还有一个在被处理中）全部都已经被标记，那么要看看是不是有多余的服务器在setup
                        max_pos = server_state[2].index(max(server_state[2]))
                        max_val = server_state[2][max_pos]
                        if(server_state[2][max_pos] != -1):
                            server_state[1][max_pos] = "OFF"
                            server_state[2][max_pos] = -1
                        # 如果找到了就修改对应服务器的状态
                        for i in range(time_point, len(time_line)):
                            if(time_line[i][0] == max_val and time_line[i][1] == "setup_until"):
                                list_of_idle_service.append(time_line[i][-2])
                                list_of_idle_service = list(set(list_of_idle_service))
                                # 既然把服务器关闭了，那么就在空闲服务器列表中把这些服务器加上
                                del time_line[i]
                                # 上面已经把多余的setup的服务器关闭了，接下来就是在时间线中将有关这些服务器的时间线移除
                                break
                time_point += 1
                # 移动到下一个时间点
            else:
                # 如果队列中没有任务的情况
                server_state[1][time_line[time_point][-2] - 1] = "WAITING"
                server_state[2][time_line[time_point][-2] - 1] = time_line[time_point][0] + delayedoff_time
                # 如果队列中没有任务，把服务器的状态变为等待关闭
                event_wait_for_off = []
                event_wait_for_off.append(time_line[time_point][0] + delayedoff_time)
                event_wait_for_off.append("waiting_off")
                event_wait_for_off.append(time_line[time_point][-2])
                event_wait_for_off.append(time_line[time_point][0] + delayedoff_time)
                time_line.append(event_wait_for_off)
                time_line = sorted(time_line, key=lambda x: x[0])
                # 把将来要关闭服务器的这个时间信息加到时间线中
                time_point += 1
                # 移动到下一个时间点

        elif(time_line[time_point][1] == "waiting_off"):
            server_state[1][time_line[time_point][-2]-1] = "OFF"
            server_state[2][time_line[time_point][-2] - 1] = -1
            # 如果走到了某个服务器的关闭时间，那么就把这个服务器的状态更改为关闭
            time_point += 1
            # 移动到下一个时间点

        else:
            time_point += 1
            # 目前没有到达这个条件的情况

    print()
    print("最后输出的时间线是：")
    for i in range(len(time_line)):
        print(time_line[i])
    print()

    print("最后输出的服务器状态是：")
    print(server_state)
    print()

    print("最后输出的空闲服务器列表是：")
    print(list_of_idle_service)
    print()

    real_departure = sorted(real_departure, key=lambda x: x[0])
    for i in range(len(real_departure)):
        real_departure[i][0] = arrival[i]
    print("最后输出的离开表是：")
    print(real_departure)
    write_file_departure_table(real_departure, "result_departure_table.txt")
    print()

    total_spend_time = 0
    for i in range(len(real_departure)):
        total_spend_time += real_departure[i][1] - arrival[i]
    total_spend_time = [total_spend_time/len(real_departure)]
    print("平均处理时间是：")
    print(total_spend_time)
    write_file_avg_time(total_spend_time, "result_average_time.txt")
    print()

    return 1



#mode = "trace"
mode = "random"

#arrival = [10, 20, 32, 33]
#service = [1, 2, 3, 4]
#m = 3
#setup_time = 50
#delayedoff_time = 100
#
# arrival = [10, 20, 32, 33, 140]
# service = [1, 2, 3, 4, 5]
# m = 3
# setup_time = 50
# delayedoff_time = 100
#
# arrival = [10, 20, 32, 33, 140, 144]
# service = [1, 2, 3, 4, 5, 6]
# m = 3
# setup_time = 50
# delayedoff_time = 100
#
# arrival = [20, 30, 40, 50, 120]
# service = [110, 110, 5, 10, 30]
# m = 3
# setup_time = 50
# delayedoff_time = 100
#
# arrival = [20, 30, 40, 50, 120, 240]
# service = [110, 110, 5, 10, 30, 18]
# m = 3
# setup_time = 50
# delayedoff_time = 100
#
arrival = [10, 12, 14, 16]
service = [1, 4, 6, 8]
m = 5
setup_time = 3
delayedoff_time = 5

lmd = 0.35
mu = 1
time_end = 1000



result = simulation(mode, arrival, service, m, setup_time, delayedoff_time, time_end)

