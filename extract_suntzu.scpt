use framework "Foundation"
use framework "Quartz"
use scripting additions

set thePath to "/Users/genesis/.openclaw/media/inbound/file_16---b6100304-2b3f-4b1f-8270-f9c3b6fb890d.pdf"
set theURL to current application's |NSURL|'s fileURLWithPath:thePath
set thePDF to current application's PDFDocument's alloc()'s initWithURL:theURL
set thePageCount to thePDF's pageCount()
set theText to ""
repeat with i from 0 to (thePageCount - 1)
	set thePage to (thePDF's pageAtIndex:i)
	set theText to theText & (thePage's |string|() as string) & return
end repeat
return theText
