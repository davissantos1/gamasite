from django import template
import os

register = template.Library()

@register.filter(name='get_original_filename')
def get_original_filename(value):
    # Obtém o nome do arquivo com a extensão
    filename = os.path.basename(value)
    
    # Divide o nome e a extensão
    name, ext = os.path.splitext(filename)
    
    # Remove o código (após o primeiro underscore) do nome do arquivo
    name_parts = name.split('_')
    
    # Retorna o primeiro fragmento do nome (que seria o nome original do arquivo)
    return name_parts[0] + ext
