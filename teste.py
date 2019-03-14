# Sample platypus document
# From the FAQ at reportlab.org/oss/rl-toolkit/faq/#1.1

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4

width, height = A4

PAGE_WIDTH, PAGE_HEIGHT = defaultPageSize

styles = getSampleStyleSheet()
Title = "title"
pageinfo = "pageinfo"

def myFirstPage(canvas, doc):
    canvas.saveState()
    canvas.setTitle('untitled')
    #canvas.setFont('Times-Bold',16)
    #canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-108, Title)
    canvas.setFont('Times-Roman',9)
    canvas.drawString(inch, 0.75 * inch,"First Page / %s" % pageinfo)
    canvas.restoreState()
    
def myLaterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(inch, 0.75 * inch,"Page %d %s" % (doc.page, pageinfo))
    canvas.restoreState()
    
def go():
    parte1 = [['teste'] for x in range(5)]
    parte2 = [['teste2'] for x in range(5)]
    doc = SimpleDocTemplate("docteste.pdf")
    Story = []
    
    t=Table(parte1,[width-2*inch], len(parte2)*[0.4*inch])
    
    t.setStyle(
        TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.white),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ])
    )

    Story.append(t)

    Story.append(Spacer(1,0.5*inch))    

    t=Table(parte2,[width-2*inch], len(parte2)*[0.4*inch])
    
    t.setStyle(
        TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.white),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ])
    )

    Story.append(t)
    
    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
    
if __name__ == "__main__":
    go()
