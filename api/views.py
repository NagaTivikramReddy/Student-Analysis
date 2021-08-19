from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from .models import Student
from .serializers import StudentSerializer
from rest_framework.decorators import api_view
from rest_framework.views import APIView


class GetCreateStudents(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class GetAddMarks(APIView):
    def post(self, request):

        data = {}

        if request.data:
            try:
                roll_no = request.data['roll_no']
                marks = request.data['marks']
                print(marks, type(marks))

                if (marks < 0 or marks > 100):
                    return Response("Marks value should be between 0 and 100")

                object = get_object_or_404(Student, roll_no=roll_no)

                if object is not None:
                    object.marks = marks
                    object.save()

                data = {
                    'roll_no': roll_no,
                    'marks': marks,
                    'updated': True
                }
            except AttributeError and KeyError:
                return Response("Please use the valid key names")
        else:
            data = "No data provided. Please provide the data"

        return Response(data)

    def get(self, request):

        counter = 1
        data = {}
        student_objects = Student.objects.all()
        for object in student_objects:
            data[counter] = {
                "roll_no": object.roll_no,
                "marks": object.marks,
                "name": object.name
            }
            counter += 1
        return Response(data.values())


@api_view(['GET'])
def GetFinalReport(request):
    data = {}
    student_objects = Student.objects.all()
    student_count = student_objects.count()
    if student_count == 0:
        return Response(data)

    GradeA_Count = 0
    GradeB_Count = 0
    GradeC_Count = 0
    GradeD_Count = 0
    GradeE_Count = 0
    GradeF_Count = 0

    for object in student_objects:
        if object.marks >= 91:
            GradeA_Count += 1
        elif object.marks >= 81:
            GradeB_Count += 1
        elif object.marks >= 71:
            GradeC_Count += 1
        elif object.marks >= 61:
            GradeD_Count += 1
        elif object.marks >= 55:
            GradeE_Count += 1
        else:
            GradeF_Count += 1

    print(GradeA_Count, GradeB_Count, GradeC_Count,
          GradeD_Count, GradeE_Count, GradeF_Count)

    distinction_percentage = GradeA_Count / student_count
    first_class_percentage = (GradeB_Count + GradeC_Count) / student_count

    pass_percentage = (student_count - GradeF_Count) / student_count

    data['student_count'] = student_count
    data['GradeA_Count'] = GradeA_Count
    data['GradeB_Count'] = GradeB_Count
    data['GradeC_Count'] = GradeC_Count
    data['GradeD_Count'] = GradeD_Count
    data['GradeE_Count'] = GradeE_Count
    data['GradeF_Count'] = GradeF_Count
    data['distinction_percentage'] = distinction_percentage * 100
    data['first_class_percentage'] = first_class_percentage * 100
    data['pass_percentage'] = pass_percentage * 100

    return Response(data)
