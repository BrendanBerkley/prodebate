from .models import *

class SampleData(object):

    def create_basics(self):
        position1 = Position.objects.create(position_statement="School uniforms should be mandated.")
        position1.tags.add('school-uniforms')
        position2 = Position.objects.create(position_statement="Wearing school uniforms does not restrict student individuality.")
        position2.tags.add('school-uniforms')
        position3 = Position.objects.create(position_statement="Students need to be able to express their individual style.")
        position3.tags.add('school-uniforms')
        position4 = Position.objects.create(position_statement="Wearing school uniforms eliminates discrimination because of what a student is wearing.")
        position4.tags.add('school-uniforms')
        position5 = Position.objects.create(position_statement="Wearing school uniforms can save parents on clothing costs.")
        position5.tags.add('school-uniforms')
        position6 = Position.objects.create(position_statement="Hitler favored school uniforms.")
        position6.tags.add('school-uniforms')
        position7 = Position.objects.create(position_statement="School uniforms are unlikely to completely eliminate discrimination via clothing.")
        position7.tags.add('school-uniforms')

        elaboration1 = Elaboration.objects.create(
            tree_relation='C',
            elaborates=position3,
            child_of=position1,
            elaboration="Adolescence is a time of self discovery. Discovering which cliques and sub groups one fits into can be a formative experience."
        )
        elaboration2 = Elaboration.objects.create(
            tree_relation='S',
            elaborates=position2,
            child_of=position1,
            elaboration="Student individuality can be expressed in other ways: Hairpieces, shoes, backpacks."
        )
        elaboration3 = Elaboration.objects.create(
            tree_relation='S',
            elaborates=position4,
            child_of=position1,
            elaboration="Students tend to value fashion and style, and will often use it as a means to discriminate. If a student (presumably a student's parent/parents) is able to afford more expensive clothing, that will often confer higher status to him and give him a reason to feel superior to a child who is unable to afford the same clothing. If all students must wear the same clothing, the gaps between Walmart shirts and Armani shirts will be greatly reduced."
        )
        elaboration4 = Elaboration.objects.create(
            tree_relation='S',
            elaborates=position5,
            child_of=position1
        )
        elaboration5 = Elaboration.objects.create(
            tree_relation='C',
            elaborates=position6,
            child_of=position1,
            elaboration="We don't want to be like Hitler right?"
        )
        elaboration6 = Elaboration.objects.create(
            tree_relation='C',
            elaborates=position7,
            child_of=position4,
            elaboration="If the uniform policy is \"red polo, khaki pants,\" then the rich kids will go for the Express polo while the poor kids go for the Walmart polos. If the school provides the red polos and khaki pants, then perhaps shoes, belts, jewelry, or other accessories will become the status symbols that kids can use to discriminate. If all clothing is regulated, then perhaps haircuts or glasses could become a status symbol. Unless every student is forced into wearing the exact same thing, school uniforms are not guaranteed to have the desired effect. "
        )
