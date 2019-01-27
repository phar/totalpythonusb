
to use:
	
	export binary format, export CSV format to the same filename (csv extention)

	export options to remember:
		X  Export Only Full Matches
		O  Export Only Visible Records
		O  Mirror Column Layout


	you can change these, but they hav to be the same for both formats, and I would ensure that mirror column layout is unchecked
even though it /should/ be handled either way.


it probably worth noting that the parser doesnt support eevery encapsulation that totalphase groups packets.. maybe i'll
take another stab at it when it matters, but it should cover most low level packets

oh.. yeah.. you also need to remove the fucking comment lines from the CSV with the exception of the 
"# Level,Sp,Index,m:s.ms.us,Dur,Len,Err,Dev,Ep,Record,Data,Summary,ASCII" line, which is used by
the script to know which column is which
