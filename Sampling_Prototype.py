def CreateCusSamples(self, NumOfSamples, DistinctField, SSplit = 1):
        DistinctField = 1
        type_9778 = 0
        type_9779 = 0
        type_9781 = 0
        type_9784 = 0
        type_9785 = 0

        curr_fileoutput = self.add_output_filetype(disp_type='FTP')

        tabidx = TabIndex(self._APPID)
        idx = Index(self._APPID)

        tabidx.get_index()
        idx.get_index()

        new_vpfind =  self._dir + self._pathSep + self._TechsortProcessDir + self._pathSep + curr_fileoutput + self._vpfFileExtn + self._indexFileExtn

        #vpf_ind_file = open(new_vpfind, "w")

        idx_pattern = self._dir + self._pathSep + self._TechsortProcessDir + self._pathSep + '*' + self._indexFileExtn

        for ts_idx in glob.glob(idx_pattern):
            splitnum = ts_idx.split("-")[1]
            if int(splitnum[1:]) == SSplit:
                with open(new_vpfind, "wb") as vpf_ind_file:
                    firstrec = True
                    for rec_line in csv.reader(open(ts_idx, "rb"), delimiter='\t', quoting=csv.QUOTE_NONE):
                        rec = "\t".join(rec_line)
                        if firstrec:
                            vpf_ind_file.write(rec +"\n")
                            firstrec = False
                            continue
                        outrec = ""
                        
                        filler1 = tabidx.getTS(rec_line, 'LETTERCODE')
                        #vpf_ind_file.write(filler1+"\n")
                        #vpf_ind_file.write(rec+"\n")
                        #vpf_ind_file.write("Hello \n")

                        if str(filler1) == "9778" and type_9778 < NumOfSamples:
                            vpf_ind_file.write(rec + "\n")
                            type_9778 += 1
                            continue
                        if str(filler1) == "9779" and type_9779 < NumOfSamples:
                            vpf_ind_file.write(rec + "\n")
                            type_9779 += 1
                            continue
                        if str(filler1) == "9781" and type_9781 < NumOfSamples:
                            vpf_ind_file.write(rec + "\n")
                            type_9781 += 1
                            continue
                        if str(filler1) == "9784" and type_9784 < NumOfSamples:
                            vpf_ind_file.write(rec + "\n")
                            type_9784 += 1
                            continue
                        if str(filler1) == "9785" and type_9785 < NumOfSamples:
                            vpf_ind_file.write(rec + "\n")
                            type_9785 += 1
                            continue
                    vpf_ind_file.close()

        # print idx._recs
        if 'EOR' not in idx._recs:
            print "No EOR Found!"
            sys.exit(9)

        idxFields = idx.get_indexFields()
        idxFields1 = idxFields.copy()
        idxFields1.pop('EOR')

        out_name = new_vpfind.replace("vpf.ind", "flat.idx")
        outfile = open(out_name, "wb")
        firstrec = True

        for rec in csv.reader(open(new_vpfind, "rb"), delimiter='\t'):
            if firstrec:
                firstrec = False
                continue
            if 'enhancement' not in rec[2]:
                continue
            outrec = ""

            filler1 = tabidx.getTS(rec, "FILLER1")
            filler1 = filler1.rjust(20)

            for indkey in idxFields1:
                outrec = idx.set(outrec, indkey, tabidx.getTS(rec, indkey))

            outrec = idx.set(outrec, "DATAREF", filler1)

            outfile.write(outrec)

        outfile.close()
