def create_pdf_buffer(remetente, destinatario, title):
    # Sample platypus document
    # From the FAQ at reportlab.org/oss/rl-toolkit/faq/#1.1

    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    from reportlab.rl_config import defaultPageSize
    from reportlab.lib.units import inch
    from reportlab.lib.pagesizes import A4
    import io

    width, height = A4

    PAGE_WIDTH, PAGE_HEIGHT = defaultPageSize

    styles = getSampleStyleSheet()

    ############
    def editCanvas(canvas, doc):
        canvas.saveState()
        canvas.setTitle(title)
        canvas.restoreState()

    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    
    Story = []
    
    t=Table(destinatario,[width-2*inch], len(destinatario)*[0.4*inch])
    
    t.setStyle(
        TableStyle([
            ('BACKGROUND',(0,0),(0,0),colors.gray),
            ('TEXTCOLOR',(0,0),(0,0),colors.white),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.white),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ])
    )

    Story.append(t)

    Story.append(Spacer(1,0.5*inch))    

    t=Table(remetente,[width-2*inch], len(destinatario)*[0.4*inch])
    
    t.setStyle(
        TableStyle([
            ('BACKGROUND',(0,0),(0,0),colors.gray),
            ('TEXTCOLOR',(0,0),(0,0),colors.white),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.white),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ])
    )

    Story.append(t)
    
    doc.build(Story, onFirstPage=editCanvas)
    
    return buffer