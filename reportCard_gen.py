#Written by Feras Yahya. A software that reads a series of CSV files and generates a student report card in the form of a JSON string outputted to a file

import pandas
import json
import sys
import functions as fn

'''
Main function
'''

def main():

    #Detects if user inputs the incorrect number of arguments and returns an error message.
    if len(sys.argv) != 6:
        return print(f"Invalid number of arguments {len(sys.argv)}. 6 Requyired!")

    #Store files into a file list by calling the read_files function with command line arguments as input
    file_list = fn.read_files(sys.argv)

    #Convert files into JSON files for easier manipulation of data later on. Create a JSON_Files list that is the same size as the file list created when reading the files
    JSON_Files = list(range(len(file_list)))
    for idx, name in enumerate(file_list):
        #Open each JSON file and store its content in a list. Note index 0 is courses file, 1 is students file, 2 is tests file and 3 is marks file
        with open(name, 'r') as file:               
            JSON_Files[idx] = json.load(file)

    if (not fn.weight_validator(JSON_Files[2])):
        errorMssg = { "error": "Invalid course weights" }       
        with open(sys.argv[5], "w+") as output2:
            output2.write(json.dumps(errorMssg))
            return print(errorMssg)                 #Return an error if total weight of a course is not 100
    
    idlist = []             #A list for storing each student's ID
    if (JSON_Files[1]["id"].items()):               #Check if the student file contains no students, this will return an error
        for x,y in JSON_Files[1]['id'].items():
            dict = { 'id': y, 'name' : JSON_Files[1]['name'][str(x)], 'total average' : 0, 'courses': []}
            idlist.append(dict)
    else:
        return print("Invalid number of students")

    course_info = {}                                
    course_list = []

    cur_id = 0                                              #main loop index
    cur_std_id = JSON_Files[3]['student_id'].get('0')       #Current student id
    cur_test_id = JSON_Files[3]['test_id'].get('0')         #Current test id
    cur_course_id = JSON_Files[2]['course_id'].get(str(cur_test_id-1))

    course_total = 0                                        #Calculates course total
    total_avg = 0                                           #Total average of all courses
    total_courses = 0                                       #Number of courses a student has taken. Used for calculating total average
    student_counter = 0                                     #A student index used for tracking the number of students and inserting their info into the id list

    while (JSON_Files[3]['mark'].get(str(cur_id), None)):

        course_total += JSON_Files[3]['mark'].get(str(cur_id))*JSON_Files[2]['weight'].get(str(cur_test_id-1))

        #Update all counters
        cur_id += 1
        #Last iteration
        if (JSON_Files[3]['mark'].get(str(cur_id), None) == None): 
            total_courses += 1
            total_avg += (course_total/100)
            idlist[student_counter]['total average'] = total_avg/total_courses
            idlist[student_counter]['courses'] = course_list
            break
        else:
            #Update test information
            cur_test_id = JSON_Files[3]['test_id'].get(str(cur_id))         
            if (cur_course_id != JSON_Files[2]['course_id'].get(str(cur_test_id-1))):

                total_courses += 1
                course_info = {'id': JSON_Files[0]['id'].get(str(cur_course_id-1)), 'name': JSON_Files[0]['name'].get(str(cur_course_id-1)), \
                            'teacher' : JSON_Files[0]['teacher'].get(str(cur_course_id-1)), 'course average': course_total/100} 
                course_list.append(course_info)

                total_avg += (course_total/100)
                course_total = 0

                cur_course_id = JSON_Files[2]['course_id'].get(str(cur_test_id-1))
            else:
                cur_course_id = JSON_Files[2]['course_id'].get(str(cur_test_id-1))

            #Check student
            if (cur_std_id != JSON_Files[3]['student_id'].get(str(cur_id))):
                total_avg = 0
                total_courses = 0
                cur_std_id = JSON_Files[3]['student_id'].get(str(cur_id))       
                idlist[student_counter]['courses'] = course_list
                student_counter +=1

            else:
                cur_std_id = JSON_Files[3]['student_id'].get(str(cur_id)) 

    students = {'students' : idlist}

    with open(sys.argv[5], "w+") as output2:
        output2.write(json.dumps(students))

    jsonstring = json.dumps(students)                                         #Final JSON string

    print(jsonstring)

if __name__ == '__main__': main()