
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# @TODO
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def make_csv_breakdown(path_csv, filename, d,  key_header):
    cwd = os.getcwd()
    make_dir(path_csv)

    with open("{path}{slash}{filename}.csv".format(path="{cwd}/{path}".format(cwd=cwd, path=path_csv), slash=('/' if path_csv else None), filename=filename), 'w') as csvfile:

        filewriter = csv.writer(csvfile)

        values = []
        for d2 in d.values():
            for v in d2:
                #  gets rid of nan.
                if isvalid(v) and v not in values:
                    values.append(v)

        values.sort()
        values.insert(0, key_header)
        # values.insert(1, -1)
        filewriter.writerow(values)
        values.remove(key_header)

        for k, d2 in zip(d.keys(), d.values()):
            row = [""]*(len(values)+1)

            # If there is a dictionary, we begin by adding the congressperson's name to the row.
            if d2:
                row.insert(0, k)

            # Then for each date, we
            for y in d2:
                if isvalid(y):
                    row[values.index(y) + 1] = d2[y]
                # else:
                #     row[values.index(-1) + 1] = d2[y]

            filewriter.writerow(row)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# @TODO
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def make_csv(path_csv, filename, d, key_header, value_header):
    cwd = os.getcwd()
    make_dir(path_csv)

    with open("{path}{slash}{filename}.csv".format(path="{cwd}/{path}".format(cwd=cwd, path=path_csv), slash=('/' if path_csv else None), filename=filename), 'w') as csvfile:
        filewriter = csv.writer(csvfile)

        filewriter.writerow([key_header, value_header])

        for k, v in zip(d.keys(), d.values()):
            filewriter.writerow([k, v])
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

