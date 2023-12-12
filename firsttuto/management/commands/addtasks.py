from django.core.management.base import BaseCommand, CommandError
from firsttuto.models import Task
from datetime import date

class Command(BaseCommand):
    help = "Add Tasks in BD. Indicate the number of tasks."

    def add_arguments(self,parser):
        parser.add_argument("nb_tasks",nargs="+",type=int)

    def handle(self,*args,**options):
        today = date.today()
        for i in range(1,options["nb_tasks"][0]+1):
            task = Task(description="Task %d %s." % (i,today.strftime("%b-%d-%Y")))
            task.save()
        self.stdout.write(self.style.SUCCESS('Success!'))