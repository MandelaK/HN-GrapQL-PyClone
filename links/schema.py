import graphene
from graphene_django import DjangoObjectType

from .models import Link


class LinkType(DjangoObjectType):
    class Meta:
        model = Link


class Query(graphene.ObjectType):
    links = graphene.List(LinkType)

    def resolve_links(self, info, **kwargs):
        return Link.objects.all()


class CreateLink(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()

    # arguments for mutation
    class Arguments:
        url = graphene.String()
        description = graphene.String()

    # mutation method. Creates link and saves it to database
    def mutate(self, info, url, description):
        link = Link(url=url, description=description)
        link.save()

        # return CreateLink class with data just created
        return CreateLink(id=link.id, url=link.url, description=link.description)


# create mutation class with field to be resolved
class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()