#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Scott Hendrickson"
__license__="Simplified BSD"
import sys
import acscsv

class WPacsCSV(acscsv.AcsCSV):
    def __init__(self, delim, options_user, options_rules, options_lang, options_struct):
        super(WPacsCSV, self).__init__(delim)
        self.options_user = options_user
        self.options_rules = options_rules
        self.options_lang = options_lang
        self.options_struct = options_struct

    def procRecordToList(self, d):
        record = []
        try:
            if "verb" in d:
                verb = d["verb"]
            else:
                msg = "Unidentified meta message"
                for mtype in ["error", "warning", "info"]:
                    if mtype in d:
                        if "message" in d[mtype]:
                            msg = d[mtype]["message"]
                        elif "message" in d:
                            msg = d["message"]
                        continue
                    mtype = "Unidentified"
                record.append(acscsv.gnipRemove)
                record.append(mtype)
                record.append(msg)
                return record
            if verb == "delete":
                record.append(acscsv.gnipRemove)
                record.append(verb)
                record.append(self.cleanField(d["object"]["id"]))
                return record
            #
            record.append(d["id"])
            record.append(d["postedTime"])
            obj = d["object"]
            if "content" in obj:
                record.append(self.cleanField(obj["content"]))
            else:
                record.append("None")
            if "summary" in obj:
                record.append(self.cleanField(obj["summary"]))
            else:
                record.append("None")
            #
            gnip = d["gnip"]
            actor = d["actor"]
            if self.options_lang:
                glang = "None"
                if "language" in gnip:
                    glang = gnip["language"]["value"]
                record.append(glang)
            if self.options_rules:
                rules = '[]'
                if "matching_rules" in gnip:
                    rules = self.buildListString([ "%s [%s]"%(l["value"], l["tag"]) for l in gnip["matching_rules"]])
                record.append(rules)
            if self.options_struct:
                target = d["target"]
                # site
                record.append(str(target["wpBlogId"]))
                # blog link
                record.append(str(target["link"]))
                # object
                record.append(str(obj["wpPostId"]))
                # link to post
                record.append(str(obj["link"]))
            if self.options_user:
                tmp = self.splitId(actor["id"])
                record.append(tmp)
            #
            return record
        except KeyError:
            sys.stderr.write("Field missing from record (%d), skipping\n"%self.cnt)
            record.append(acscsv.gnipError)
            return record

