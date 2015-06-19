import pandas as pd


def load_fec(subsample=True):
    if subsample:
        fec = pd.read_csv("../data/fec_subsample.csv.gz", compression="gzip")
    else:
        fec = pd.read_csv("../data/P00000001-ALL.csv.gz", compression="gzip",
                          index_col=False)
    # drop presumed duplicates
    fec = fec.groupby('tran_id', as_index=False).first()
    return fec


def clean_fec(fec, parse_dates=False):
    fec.rename(columns=dict(contbr_city='city',
                            contbr_st='state',
                            contbr_zip='zip',
                            contbr_employer='employer',
                            contb_receipt_amt='amount',
                            contb_receipt_dt='date',
                            contbr_occupation='occupation',
                            contbr_name='name',
                            cand_name='candidate',
                            ), inplace=True)

    to_replace = {'33': 'FL',
                  '46': 'IN',
                  '48': 'MI',
                  '49': 'MI',
                  '7': 'NJ',
                  '77': 'LA',
                  '8': 'NJ',
                  '84': 'UT',
                  '91': 'CA'}

    fec = fec.ix[fec.election_tp.str.match('G2012', na=False)]
    fec.replace(to_replace=dict(state=to_replace), inplace=True)

    if parse_dates:
        fec['date'] = pd.to_datetime(fec.date)
    return fec

if __name__ == "__main__":
    fec = clean_fec(load_fec(), parse_dates=False)
