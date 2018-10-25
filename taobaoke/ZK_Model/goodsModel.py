# import ZK_Model.ZKOrderDataModel
# p = ZK_Model.ZKOrderDataModel.userData()
import  threading
def get():
    for i in range(1,20):
        # print(i)
        if i != 50:
            print(i)
            # return i

    print(123)
get()