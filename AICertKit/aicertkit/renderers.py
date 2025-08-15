def render_model_card(ctx):
    return f"# Model Card: {ctx['repo_name']}\n\nGenerated: {ctx['generated']}\n"

def render_data_card(ctx):
    return f"# Data Card: {ctx['repo_name']}\n\nGenerated: {ctx['generated']}\n"

def render_risk_yaml(risk):
    import json
    return 'generated: '+risk['generated']+'\nrepo: '+risk['repo']+'\n'
