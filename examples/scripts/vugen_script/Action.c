Action() {

    lr_start_transaction("Transaction_01");

	web_url("www.example.com",
	    "URL=http://www.example.com",
	    "Snapshot=t10.inf",
	    LAST);

    lr_end_transaction("Transaction_01", LR_AUTO);

    lr_start_transaction("Transaction_02");

    web_url("www.example.com",
	    "URL=http://www.example.com",
	    "Snapshot=t20.inf",
	    LAST);

	lr_end_transaction("Transaction_02", LR_AUTO);

    lr_start_transaction("Transaction_03");

    web_url("www.example.com",
	    "URL=http://www.example.com",
	    "Snapshot=t30.inf",
	    LAST);

    lr_end_transaction("Transaction_03", LR_AUTO);


	return 0;
}
