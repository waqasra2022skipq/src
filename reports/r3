select Treatment.TrID, Treatment.BillDate, Treatment.BillStatus, Treatment.RecDate, Treatment.BilledAmt, Treatment.AmtDue
,NoteTrans.ID, NoteTrans.InsCode, NoteTrans.RecDate, NoteTrans.PaidAmt, NoteTrans.Code, NoteTrans.SRC
from NoteTrans
  left join Treatment on Treatment.TrID=NoteTrans.TrID
where Treatment.BillStatus!=3
and NoteTrans.RecDate is null
and NoteTrans.PaidAmt is null
order by Treatment.BillStatus, Treatment.RecDate, Treatment.TrID
