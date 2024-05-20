select Provider.ProvID,Provider.Name
      ,ProviderEDocs.Type,ProviderEDocs.Title,ProviderEDocs.Descr
 from ProviderEDocs
  left join Provider on Provider.ProvID=ProviderEDocs.ProvID
 where Provider.Type IN (2,3)
 order by Provider.Name
;
