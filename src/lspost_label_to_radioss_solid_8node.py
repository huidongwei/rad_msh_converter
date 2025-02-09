import pandas as pd


#input file name & open it for reading
file_name = input("Please input the raw k file (without .k): ")
my_input = open(file_name + ".k","r")

#new file name & open it for writing
my_file = open(file_name +"_new_relabel"+".inc","w")

#detect the node label &
Node_label = False
#detect the node re-order marking
node_reorder = 0

#detect the shell elements re-order marking
Shell_label = False

#detect the group nodes re-order marking
Gnode_label = False
Gshel_label = False

#
Seg_label = False
Seg_start = int(1)

#record the line readings
line_num = 0

#define the initial starting nodes and elements label
#start_node = int(input("Input the node label ini-number: "))
#start_elem = int(input("Input the element label ini-number: "))
#scale = float(input("Input scaling factor of the nodes coordinate: "))

#X_trans = float(input("Input translation of X_coordinate: "))

old_part = int(0)
shell_3 = 0

df = pd.DataFrame(columns=['part', 'cat', 'label','node_1', 'node_2',
                            'node_3', 'node_4', 'node_5', 'node_6',
                            'node_7', 'node_8'])

df_node = []
#main loop of the input file
for line in my_input:

    #line = f.read()
    #print(line)
    
    line_num = line_num+1
    
    new_line = line

    #check if node label observed    
    if "DEF_NODE" in line and not("SET_NODE" in line): 
        print("node definition found in line {0:5d}".format(line_num))
        Node_label  = True
        Shell_label = False
        Gnode_label = False
        Gshel_label = False
        Seg_label = False
        
        #my_file.write(line)
        #node_reorder = node_reorder + 1  
        
    #check if element label observed    
    elif "ELEMENT_SOLID" in line and not("SET_SOLID" in line): 
        print("shell definition found in line {0:5d}".format(line_num))
        Shell_label = True
        Node_label  = False
        Gnode_label = False
        Gshel_label = False
        Seg_label = False
        
        #my_file.write(line)
        #node_reorder = 0

    elif "SET_NODE_LIST_TITLE" in line: 
        print("group node definition found in line {0:5d}".format(line_num))
        Gnode_label = True
        Shell_label = False
        Node_label  = False
        Gshel_label = False
        Seg_label = False

    elif "SET_SOLID_TITLE" in line: 
        print("group shell definition found in line {0:5d}".format(line_num))
        Gshel_label = True
        Gnode_label = False
        Shell_label = False
        Node_label  = False
        Seg_label = False        

    elif "SET_SEGMENT_TITLE" in line: 
        print("segment definition found in line {0:5d}".format(line_num))
        Seg_label = True         
        Gshel_label = False
        Gnode_label = False
        Shell_label = False
        Node_label  = False
       
    #############################################################
    #re-order all the nodes if node label observed from next line
    #############################################################
    if Node_label:        
        #new_line = line
        data = new_line.split()
        # print(data)
        
        if data[0].isnumeric():
        
            node = int(data[0])
            node_X = float(data[1])
            node_Y = float(data[2])
            node_Z = float(data[3])
            
            new_line = "{0:10d}".format(node)+"{0:20.5e}".format(node_X)+\
                   "{0:20.5e}".format(node_Y)+"{0:20.5e}".format(node_Z)+'\n'
               
        #my_file.write(new_line)   

    #############################################################
    #re-order all the elements if elements label observed from next line
    #############################################################
          
    if Shell_label:
        
        #new_line = line
        data = new_line.split()
        
        #print(data)
        if data[0].isnumeric():
            
            element = int(data[0])
            
            new_part = int(data[1])
            
            node_1 = int(data[2])
            node_2 = int(data[3])
            node_3 = int(data[4]) 
            node_4 = int(data[5])
            node_5 = int(data[6])
            node_6 = int(data[7])
            node_7 = int(data[8])
            node_8 = int(data[9])
            
            new_line = ''
            
            new_line = new_line + "{0:10d}".format(element)+\
                "{0:10d}".format(node_1)+\
                    "{0:10d}".format(node_2)+\
                        "{0:10d}".format(node_3)+\
                        "{0:10d}".format(node_4)+\
                        "{0:10d}".format(node_5)+\
                        "{0:10d}".format(node_6)+\
                        "{0:10d}".format(node_7)+\
                        "{0:10d}".format(node_8)+'\n'            
            
            if node_3==node_4:
                
                cat = 0
                
            else:
                
                cat = 1
            
            df_new = pd.DataFrame([{'part':new_part, 'cat':cat, 'label': element,
                                   'node_1':node_1,'node_2':node_2,
                                   'node_3':node_3,'node_4':node_4,
                                   'node_5':node_5,'node_6':node_6,
                                   'node_7':node_7,'node_8':node_8}])
            
            df = pd.concat([df,df_new], ignore_index=True)
            
            # new_line=''
            
            
            
            # if new_part != old_part or shell_3 == 1:
            #     my_file.write('/SHELL/' + str(new_part) + '\n')
            #     old_part = new_part
            #     shell_3 = 0
            
            # if node_3 == node_4:
            #     my_file.write('/SH3N/' + str(new_part) + '\n')
            #     shell_3 = 1

            # new_line = "{0:10d}".format(element)+"{0:10d}".format(node_1)+\
            #        "{0:10d}".format(node_2)+"{0:10d}".format(node_3)+\
            #           "{0:10d}".format(node_4) + '\n'
               
        #my_file.write(new_line)  
        
    if Gnode_label:
        #new_line = line
        data = new_line.split()
        
        if data[0].isnumeric() and data[4].isnumeric():
        
            m = len(data)
            
            new_line = ''
            
            for i in range(m):
                
                new_line = new_line + "{0:10d}".format(int(data[i]))
                
                if i%9==0 and i!=0:   
                    
                    new_line = new_line + '\n'
                
            new_line = new_line + '\n'

    if Gshel_label:
        #new_line = line
        data = new_line.split()
        
        if data[0].isnumeric() and (type(data[1]) is int):
        
            m = len(data)
            new_line = ''
            
            for i in range(m):
                
                new_line = new_line + "{0:10d}".format(int(float(data[i])))
                
                if i%9==0 and i!=0:   
                    
                    new_line = new_line + '\n'
                
            new_line = new_line + '\n'
    
    if Seg_label:

        data = new_line.split()
        print(data)
        
        if data[0].isnumeric() and data[3].isnumeric():
        
            m = len(data)
            
            new_line = ''
            
            
            new_line = new_line + "{0:10d}".format(int(Seg_start)) +\
                                "{0:10d}".format(int(float(data[0])))+\
                                "{0:10d}".format(int(float(data[1])))+\
                                "{0:10d}".format(int(float(data[2])))+\
                                "{0:10d}".format(int(float(data[3])))+'\n'
            
            Seg_start = Seg_start + 1
            
            
            # for i in range(4):
                
            #     new_line = new_line + "{0:10d}".format(int(float(data[i])))
                
                             
            # new_line = new_line + '\n'        
            
    my_file.write(new_line)
      
my_file.close()          
        