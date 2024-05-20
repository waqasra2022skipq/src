  select ClientPHQ9.*
        ,Provider.Name as Clinic
        ,Client.ClientID
        ,Client.LName, Client.FName, Client.ClientID, Client.Active
        ,Client.Addr1, Client.Addr2, Client.City, Client.ST, Client.Zip
        ,Client.HmPh, Client.WkPh
        ,Client.DOB, Client.Gend, xRaces.Descr as Race, Client.SSN
        ,truncate((to_days(curdate()) - to_days(Client.DOB)) / 365,0) as Age
        ,Client.ProvID as PrimaryProvID
        ,Client.clinicClinicID
  from ClientPHQ9
    left join Client on Client.ClientID=ClientPHQ9.ClientID
    left join ClientACL on ClientACL.ClientID=Client.ClientID
    left join Provider on Provider.ProvID=Client.clinicClinicID
    left join okmis_config.xRaces on xRaces.ID=SUBSTRING_INDEX(Client.Race,'ý',1)
    left join ClientPrAuth on ClientPrAuth.ClientID=Client.ClientID
    left join ClientPrAuthCDC on ClientPrAuthCDC.ClientPrAuthID=ClientPrAuth.ID
    left join Insurance on Insurance.InsNumID=ClientPrAuth.InsuranceID
    left join xInsurance on xInsurance.ID=Insurance.InsID
  where ClientACL.ProvID='91'
    and  (  Client.clinicClinicID=2359  ) and  (  xInsurance.ID=100  ) and Client.Active=1
    and ClientPrAuth.PAnumber is not null
    and curdate() between ClientPrAuth.EffDate and ClientPrAuth.ExpDate
    and (ClientPrAuthCDC.TransType=23 || ClientPrAuthCDC.TransType=42)
  order by Provider.Name, Client.LName, Client.FName, ClientPHQ9.TestDate desc
