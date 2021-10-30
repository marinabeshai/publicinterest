
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# @TODO
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def graph_csv(path_csv, path_html, filename, key_header, value_header, type="normal"):
    cwd = os.getcwd()
    make_dir(path_html)

    name = "{path}{slash}{filename}.csv".format(path="{cwd}/{path}".format(
        cwd=cwd, path=path_csv), slash=('/' if path_csv else None), filename=filename)

    df = pd.read_csv(name)

    if type != "normal":
        fig = px.scatter(df, x=key_header, y=value_header, title='')
    else:
        fig = px.line(df, x=key_header, y=value_header, title='')

    fig.write_html("{path}{slash}{filename}.html".format(path="{cwd}/{path}".format(
        cwd=cwd, path=path_html), slash=('/' if path_html else None), filename=filename))

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
