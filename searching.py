from data import HEADING
from state_and_node import Node

class Stack:
    #Tạo một danh sách rỗng để lưu trữ các phần tử.
    def __init__(self):
        self.list = []

    #Thêm phần tử vào đỉnh của Stack.
    def push(self,item):
        self.list.append(item)

    #Loại bỏ phần tử cuối cùng của Stack.
    def pop(self):
        return self.list.pop()

    #Kiểm tra xem Stack trống
    def isEmpty(self):
        return len(self.list) == 0

class SearchPuzzle:
    def generateNode(self, current:Node)->list:
        '''
        Hàm tạo ra tất cả các nút có thể có do việc thay đổi góc quay ở mỗi vị trí trong lưới.
        '''
        ans = []
        for i in range(5):
            for j in range(5):             
                for k in HEADING:                   
                    if current.state.head[i][j]["heading"] == k:
                        continue   
                    newNode = Node(current.state.head,[i,j],current)

                    newNode.state.head[i][j]["heading"] = k
                    newNode.state.triggledAt([i, j])
                    newNode.step = current.step + 1
                    ans.append(newNode)
        return ans
    def getPath(self, end_node: Node)->list:
        '''
        Hàm di chuyển ngược từ nút cuối về nút bắt đầu, thu thập các trạng thái trên đường đi
            và trả về chúng theo đúng thứ tự.
        '''
        ans = []
        temp = end_node
        while temp:
            ans.insert(0,temp.state)
            temp = temp.previous
        return ans

    def hx(self, current: Node)->int:
        ans = 0
        ans = ans - 5* current.state.countBump
        #kiểm tra trạng thái hiện tại (current) và trạng thái cha (parrent)
        if current.previous != None:
            if current.state.countBump == current.previous.state.countBump:
                s = False
                for i in range(5):
                    for j in range(5):
                        if current.state.head[i][j]["bump"] != current.previous.state.head[i][j]["bump"]:
                            ans -= 2
                            s = not(s)
                        elif current.state.head[i][j]["bump"] and current.previous.state.head[i][j]["bump"]:
                            if current.state.head[i][j]["heading"] != current.previous.state.head[i][j]["heading"]:
                                ans -= 2
                                s = not(s)
                        if s:
                            break
                    if s:
                        break
                if not(s):
                    ans += 2
        #Kiểm tra số lượng ống không khả thi ở viền
        if current.state.countBump:
            for i in [0,4]:
                for j in range(5):
                    list1 = current.state.getAngle(current.state.head[i][j])
                    if i == 0:
                        if 90 in list1:
                            ans += 1
                            if current.state.head[i][j]["bump"]:
                                ans += 5
                        else:
                            ans -= 2
                    if i == 4:
                        if 270 in list1:
                            ans += 1
                            if current.state.head[i][j]["bump"]:
                                ans += 5
                        else:
                            ans -= 2
            
            for j in [0,4]:
                for i in range(5):
                    list1 = current.state.getAngle(current.state.head[i][j])
                    if j == 0 and 180 in list1:
                        ans += 1
                        if current.state.head[i][j]["bump"]:
                            ans += 5
                    else: ans -= 2
                    if j == 4 and 0 in list1:
                        ans += 1   
                        if current.state.head[i][j]["bump"]:
                            ans += 5
                    else:
                        ans -= 2     

        #Kiểm tra vòng lặp ống bump
        if current.state.checkRecursionBump(current.rotate[0], current.rotate[1]):
            ans += 2000
        return ans 

    def gx(self, current: Node):
        if current == None:
            return 0
        return current.step*2

    def fx(self, current: Node) -> int:
        return self.gx(current) + self.hx(current)

    def solve_Astar(self, init_state: list):
        # Khởi tạo trạng thái ban đầu đặt ở trung tâm
        head = Node(init_state, [2,2], None)
        #Áp dụng heuristic f(x) ước lượng chi phí
        head.heuristics = self.fx(head)
        #Đặt bước của trạng thái ban đầu được đặt là 0
        head.step = 0

        #Khởi tạo openList chứa trạng thái mới
        openList = [[self.fx(head),head]]
        #Khởi tạo 'dataForPlot' để thu thập số bước
        dataForPlot = {0:1}
        #Khởi tạo closeList chứa các trạng thái đã được duyệt
        closeList = []

        while len(openList) != 0:
            #Lấy trạng thái từ openList để kiểm tra
            current_state = openList.pop(0)

            #Nếu chưa có trong dataForPlot thì gán giá trị
            if current_state[1].step not in dataForPlot:
                dataForPlot.update({current_state[1].step:1})
            #Nếu có thì tăng giá trị lên 1
            else:
                dataForPlot[current_state[1].step] += 1
            #Kiểm tra nếu trạng thái chưa được duyệt
            if current_state[1] not in closeList:
                #Là trạng thái mục tiêu thì dừng và in 'Successfully'
                closeList.append(current_state[1])
                if current_state[1].state.countBump == 25:
                    print("Successfully")
                    break

                #Nếu không thì sinh trạng thái mới
                newStateList = self.generateNode(current_state[1])
                #Kiểm tra đã duyệt qua hay có trong openList chưa nếu chưa thì thêm vào openList
                for newNode in newStateList:
                    if newNode not in closeList and newNode not in(obj for obj in openList):
                        openList.append([self.fx(newNode), newNode])

                #Sắp xếp openList có giá trị heuristics tăng dần để ưu tiên giá trị nhỏ nhất
                openList.sort(key=lambda x: int(x[0]))

        #In ra tổng số trạng thái
        print("Number of state: ", len(openList) + len(closeList))

        #Trả về kết quả
        return dataForPlot, self.getPath( closeList.pop(len(closeList) - 1))

    def solve_dfs(self, init_state: list)->list:
        """
        DFS for the path from init_state to goal_state and save in self.path
        """
        open_list = Stack()
        visited = []
        first_node = Node(init_state, [0,0], None)
        open_list.push(first_node)
        #count = 0
        while not open_list.isEmpty():
            #count += 1
            #if (count == 100):
            #    break
            current_node = open_list.pop()
            visited.append(current_node)

            print(len(open_list.list))
            if current_node.state.countBump == 25:
                return self.getPath(current_node)
            
            successors = self.generateNode(current_node)
            for item in successors:
                if item not in visited and item not in open_list.list:
                    open_list.push(item)     
        return self.getPath(visited[len(visited) - 1]) 