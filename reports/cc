select Contracts.InsID, Provider.ProvID, Provider.Name
,xInsurance.Name, xInsurance.Descr
,Contracts.BillType, xInsurance.RecID
      #,Contracts.UseSpecialty,Contracts.UseReferring,Contracts.UseRendering,Contracts.UseSFacility
      #,ProviderControl.NPI,Contracts.TaxID,Contracts.PIN,Contracts.SourceCode,Provider.Name
 from Contracts
  left join xInsurance on xInsurance.ID=Contracts.InsID
  left join Provider on Provider.ProvID=Contracts.ProvID
  left join ProviderControl on ProviderControl.ProvID=Contracts.ProvID
 where Provider.Active=1 
#   and (Contracts.BillType='BH' or Contracts.BillType='RH')
   and Provider.ProvID=229
   and xInsurance.ID=414
#   and xInsurance.Descr='bcbsok'
 #order by xInsurance.Descr,ProviderControl.NPI;
 order by Provider.Name;
