sub getP
{
  my ($self,$p,$TrID) = @_;

my $x_table = 55;
my $tablewidth = 475;

my $fontsize = 10;

my $fontname= "{New Times Roman}";
my $basefontoptions = "";
my $optlist;

my @headers = ( "ICD10", "NAME", "INITIATED", "RESOLVED");
my @alignments = ( "center", "left", "center", "center");

        $basefontoptions = "fontname=" . $fontname . " fontsize=" . 
            $fontsize . " embedding encoding=unicode";

        # -----------------------------------
        # Create and place table with article list
        # -----------------------------------
        
        # ---------- Header row 
        my $row = 1;
        my $col = 1;
        my $tbl = -1; 
        my $buf;

        for ($col=1; $col <= $#headers+1; $col++)
        {
            $optlist =  "fittextline={position={" . $alignments[$col-1] . 
                " center} " . $basefontoptions . "} margin=2";
            $tbl = $p->add_table_cell($tbl, $col, $row, $headers[$col-1], 
            $optlist);
        }
        $row++;

        # ---------- Data rows: one for each article 
        my $total = 0;

        for (my $i = 0; $i <  $#data+1; $i++) {
            $col = 1;

            # column 1: ITEM 
            $buf = sprintf("%d", $i + 1);
            $optlist = "fittextline={position={" . $alignments[$col-1] . 
                " center} " . $basefontoptions . "} margin=2";
            $tbl = $p->add_table_cell($tbl, $col++, $row, $buf, $optlist);

            # column 2: DESCRIPTION 
            $optlist = "fittextline={position={" . $alignments[$col-1] . 
                " center} " . $basefontoptions . "} colwidth=50% margin=2";
            $tbl = $p->add_table_cell($tbl, $col++, $row, $data[$i]{name},
                    $optlist);

            # column 3: QUANTITY 
            $buf = sprintf("%d", $data[$i]{quantity});
            $optlist = "fittextline={position={" . $alignments[$col-1] . 
                " center} " . $basefontoptions . "} margin=2";
            $tbl = $p->add_table_cell($tbl, $col++, $row, $buf, $optlist);

            # column 4: PRICE 
            $buf =  sprintf("%.2f", $data[$i]{price});
            $optlist = "fittextline={position={" . $alignments[$col-1] . 
                " center} " . $basefontoptions . "} margin=2";
            $tbl = $p->add_table_cell($tbl, $col++, $row, $buf, $optlist);

            $row++;
        }

        $optlist = "rowheight=1 margin=2 margintop=" . 2*$fontsize . 
            " textflow=" . $tf . " colspan= " . ($#headers+1);
        $tbl = $p->add_table_cell($tbl, 1, $row++, "", $optlist);


                $top = 50;

            # Place the table on the page; Shade every other row. 
            $optlist =  "header=1 fill={{area=rowodd fillcolor={gray 0.9}}} ";

            $result = $p->fit_table($tbl,
                    $x_table, $top, $x_table+$tablewidth, 20, $optlist);

            if ($result eq "_error") {
                throw new Exception("Couldn't place table: "
                    . $p->get_errmsg());
            }

        $p->delete_table($tbl, "");
}
