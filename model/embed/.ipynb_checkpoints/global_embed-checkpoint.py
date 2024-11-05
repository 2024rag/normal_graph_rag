from model.embed.autodl_embed import model
from model.embed.gs_embed import gs_embed


def embedding(sentences):
  return model.encode(sentences)