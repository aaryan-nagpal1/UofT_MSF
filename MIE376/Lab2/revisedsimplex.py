import numpy as np

def revised_simplex(c,A,b, basic, non_basic, optimize):
    c=np.matrix(c)
    A=np.matrix(A)
    b=np.matrix(b)
    non_zero_count = np.count_nonzero(c)
    x=[]
    zero_count = len(c) - non_zero_count
    B = np.empty((zero_count, zero_count))
    N = np.empty((non_zero_count,non_zero_count))
    if optimize == 'maximizing':
        k=0
        while k<(len(basic))**2-1:
            c_B= c[basic, :]
            c_N= c[non_basic, :]
            x_B = np.empty((c_B.shape[0],c_B.shape[1]))
            x_N = np.empty((c_B.shape[0],c_B.shape[1]))
            B = A[:,basic]
            N = A[:,non_basic]
            a_e=np.empty((x_B.shape[0],x_B.shape[1]))
            I=np.eye(int(zero_count))
            if (B==I).all() == True:
                B_inv = B
            else:   
                B_inv = np.linalg.inv(B)
            z_mid=np.matmul(np.transpose(c_B), (np.matmul(B_inv, N)))-np.transpose(c_N)
            print(z_mid)
            if np.all(z_mid>=0):
                x_B=np.matmul(B_inv,b)
                z=np.matmul(np.transpose(c_B),x_B)
                optimal_sol = z.item()
                for i in range(len(basic)):
                    if basic[i]<len(c_N):
                        x.append(basic[i])
                for i in range(len(non_basic)):
                    if non_basic[i]<len(c_N):
                        x.append(non_basic[i])
                var=[]
                x.sort()
                print(" ")
                print("Optimized variable values are:")
                for i in range (len(c_N)):
                    var.append(0)
                for i in range (len(c_N)):
                    if x[i] in basic:
                        p=basic.index(x[i])
                        var[i]=round(x_B[p].item(),1)
                    print("x_"+str(i+1), "=", var[i])
                print(" ")
                return optimal_sol 
            elif np.any(z_mid<0):
                min_pick = z_mid[0,0]
                min_pick_index = np.argwhere(z_mid==min_pick)[0][1]
                for i in range(1,len(c_N)):
                    if z_mid[0,i]<min_pick and z_mid[0,i]<0:
                        min_pick=z_mid[0,i]
                        min_pick_index = np.argwhere(z_mid==min_pick)[0][1]
                pick=min_pick_index
                picked=pick
                for i in range(A.shape[0]):
                    a_e=A[:,picked]
                sub_ratio = np.dot(B_inv,a_e)
                for i in range(len(basic)):
                    if sub_ratio[i][0]==0:
                        sub_ratio[i][0]=1000
                ratio_checker = np.divide(np.dot(B_inv,b),sub_ratio)
                min_ratio=ratio_checker[0][0]
                if ratio_checker[0][0]<0:
                        min_ratio=ratio_checker[1][0]
                        min_ratio_index = np.argwhere(ratio_checker==min_ratio)[0][0]
                for i in range(1,len(ratio_checker)):
                    if ratio_checker[i][0]<min_ratio and ratio_checker[i][0]>0:
                        min_ratio=ratio_checker[i][0]
                        min_ratio_index = np.argwhere(ratio_checker==min_ratio)[0][0]
                departing=min_ratio_index
                departed = departing
                temp=[]
                x_B=c[basic, :]
                x_N=c[non_basic, :]
                for i in range(len(basic)):
                    temp.append(basic[i])
                basic[departed]=non_basic[picked]
                non_basic[picked]=temp[departed]
            else:
                x_B=np.matmul(B_inv,b)
                z=np.matmul(np.transpose(c_B),x_B)
                optimal_sol = z.item()
                return optimal_sol
            k+=1
    elif optimize=='minimizing':
        k=0
        while k<(len(basic))**2-1:
            c_B= c[basic, :]
            c_N= c[non_basic, :]
            x_B = np.empty((c_B.shape[0],c_B.shape[1]))
            x_N = np.empty((c_B.shape[0],c_B.shape[1]))
            B = A[:,basic]
            N = A[:,non_basic]
            a_e=np.empty((x_B.shape[0],x_B.shape[1]))
            I=np.eye(int(zero_count))
            if (B==I).all() == True:
                B_inv = B
            else:   
                B_inv = np.linalg.inv(B)
            z_mid=np.matmul(np.transpose(c_B), (np.matmul(B_inv, N)))-np.transpose(c_N)
            if np.all(z_mid<=0):
                x_B=np.matmul(B_inv,b)
                z=np.matmul(np.transpose(c_B),x_B)
                optimal_sol = z.item()
                for i in range(len(basic)):
                    if basic[i]<len(c_N):
                        x.append(basic[i])
                for i in range(len(non_basic)):
                    if non_basic[i]<len(c_N):
                        x.append(non_basic[i])
                print(" ")
                print("Optimized variable values are:")
                var=[]
                x.sort()
                for i in range (len(c_N)):
                    if x[i] in basic:
                        j=basic.index(x[i])
                        var.append(round(x_B[j].item(),1))
                    else:
                        var.append(0)
                    print("x_"+str(i+1), "=", var[i])
                print(" ")
                return optimal_sol
            elif np.any(z_mid>0):
                max_pick = z_mid[0,0]
                max_pick_index = np.argwhere(z_mid==max_pick)[0][1]
                for i in range(1,len(c_N)):
                    if z_mid[0,i]>max_pick and z_mid[0,i]>0:
                        max_pick=z_mid[0,i]
                        max_pick_index = np.argwhere(z_mid==max_pick)[0][1]
                pick=max_pick_index
                picked=pick
                for i in range(A.shape[0]):
                    a_e=A[:,picked]
                sub_ratio = np.dot(B_inv,a_e)
                for i in range(len(basic)):
                    if sub_ratio[i][0]==0:
                        sub_ratio[i][0]=-1000
                ratio_checker = np.divide(np.dot(B_inv,b),sub_ratio)
                max_ratio=ratio_checker[0][0]
                max_ratio_index = np.argwhere(ratio_checker==max_ratio)[0][0]
                if ratio_checker[0][0]>0:
                        max_ratio=ratio_checker[1][0]
                for i in range(1,len(ratio_checker)):
                    if ratio_checker[i][0]>max_ratio and ratio_checker[i][0]<0:
                        max_ratio=ratio_checker[i][0]
                        max_ratio_index = np.argwhere(ratio_checker==max_ratio)[0][0]
                departing=max_ratio_index
                departed = departing
                temp=[]
                x_B=c[basic, :]
                x_N=c[non_basic, :]
                for i in range(len(basic)):
                    temp.append(basic[i])
                basic[departed]=non_basic[picked]
                non_basic[picked]=temp[departed]
            else:
                x_B=np.matmul(B_inv,b)
                z=np.matmul(np.transpose(c_B),x_B)
                optimal_sol = z.item()
                return optimal_sol
            k+=1
    
#Question 1
c= [[-3],
    [8],
    [0],
    [0]]
A= [[4,2,1,0],
    [2,3,0,1]]
b= [[12],
    [6]]
basic = [2,3]
non_basic = [0,1]
optimize = 'minimizing'
print("The", optimize, "solution to this optimization problem is :", revised_simplex(c,A,b, basic, non_basic, optimize))

#Question 2
c = [[3],
      [2],
      [-1],
      [-2],
      [1],
      [2],
      [-1],
      [3],
      [4],
      [-3],
      [0],
      [0],
      [0],
      [0],
      [0]]
A = [[2,1,3,1,2,1,4,1,-2,3,1,0,0,0,0], 
     [1,-4,1,2,3,1,-1,4,1,2,0,1,0,0,0], 
     [3,2,-2,-1,1,3,2,1,1,1,0,0,1,0,0], 
     [2,3,1,1,1,1,1,1,3,2,0,0,0,1,0], 
     [1,1,1,1,1,1,1,1,1,1,0,0,0,0,1]]
b = [[80],
      [50],
      [40],
      [90],
      [50]]
basic = [10,11,12,13,14]
non_basic = [0,1,2,3,4,5,6,7,8,9]
optimize = 'maximizing'
print("The", optimize, "solution to this optimization problem is :", revised_simplex(c,A,b, basic, non_basic, optimize))




