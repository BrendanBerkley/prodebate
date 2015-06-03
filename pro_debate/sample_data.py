from .models import *

class SampleData(object):

    def create_basics(self):
        position1 = Position.objects.create(position_statement="School uniforms should be mandated.")
        position2 = Position.objects.create(position_statement="Wearing school uniforms does not restrict student individuality.")
        position3 = Position.objects.create(position_statement="Students need to be able to express their individual style.")

        elaboration1 = Elaboration.objects.create(
            tree_relation='C',
            elaborates=position3,
            child_of=position1,
            elaboration="Adolescence is a time of self discovery. Discovering which cliques and sub groups one fits into can be a formative experience."
        )
