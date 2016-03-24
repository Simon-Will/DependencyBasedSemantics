#!/usr/bin/awk -f

BEGIN {
    RS = "\n\n\n"
    FS = "\n"
    ORS = ""
    OFS = ""
    PROBLEMS = 1
    print "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<fracas-problems>\n\n"
}

{
    PREMISES = 0
    ANSWER = ""

    # Get answer of problem
    if ($NF ~ /true|True/) {
        ANSWER = "yes"
    } else if ($NF ~ /false|False/) {
        ANSWER = "no"
    } else if ($NF ~ /unknown|Unknown/) {
        ANSWER = "unknown"
    } else {
        ANSWER = "???"
    }

    # Print opening tag
    print "<problem\n"
    print "  id=\"", PROBLEMS, "\"\n"
    print "  fracas_answer=\"", ANSWER, "\">\n"
    
    for (i = 1; i < NF; ++i) {
        if ($i ~ /^P:/) {
            ++PREMISES
            # Get premise info
            SENTENCE = substr($i, 4, length($i) - 3)
            CONLL_START = i + 1
            CONLL_END = i
            for (; $i !~ /^\s*$/; ++i) {
                CONLL_END = i
            }

            # Print premise info
            print "  <p idx=\"", PREMISES, "\">\n"
            print "    ", SENTENCE, "\n"
            print "  </p>\n"
            print "  <p_conll idx=\"", PREMISES, "\">"
            for (j = CONLL_START; j <= CONLL_END; ++j) {
                print $j, "\n"
            }
            print "</p_conll>\n"

        } else if ($i ~ /^H:/) {
            # Get hypothesis info
            SENTENCE = substr($i, 4, length($i) - 3)
            CONLL_START = i + 1
            CONLL_END = i
            for (; $i !~ /^\s*$/; ++i) {
                CONLL_END = i
            }

            # Print hypothesis info
            print "  <h>\n"
            print "    ", SENTENCE, "\n"
            print "  </h>\n"
            print "  <h_conll>"
            for (j = CONLL_START; j <= CONLL_END; ++j) {
                print $j, "\n"
            }
            print "</h_conll>\n"
        }
    }

    print "  <a>", ANSWER, "</a>\n"

    # Print closing tag
    print "</problem>\n\n"
    ++PROBLEMS
}

END {
    print "</fracas-problems>\n"
}
