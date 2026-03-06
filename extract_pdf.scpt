use framework "Foundation"
use framework "Quartz"
use scripting additions

set thePath to "/Users/genesis/.openclaw/workspace/Fwd_PASSAGE 1-30 双语版.pdf"
set theURL to current application's |NSURL|'s fileURLWithPath:thePath
set thePDF to current application's PDFDocument's alloc()'s initWithURL:theURL
set thePageCount to thePDF's pageCount()
set theText to ""
repeat with i from 0 to (thePageCount - 1)
	set thePage to (thePDF's pageAtIndex:i)
	set theText to theText & "--- Page " & (i + 1) & " ---" & return & (thePage's |string|() as string) & return
end repeat
return theText

on min(a, b)
	if a < b then return a
	return b
end min
