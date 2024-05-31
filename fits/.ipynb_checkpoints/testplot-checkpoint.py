import ROOT

# Open a ROOT file
file = ROOT.TFile("fits_ggh_BDTperyear__cat3/workspace_ggh_BDTperyear__cat3_background_cats_chebyshev2.root", "READ")

# Access the workspace
workspace = file.Get("w")  # Replace "workspace_name" with the actual name of your workspace
if not workspace:
    print("Workspace not found in the file.")
    file.Close()
    exit()

# Import RooFit classes
ROOT.gSystem.Load("libRooFit")

# Access the datasets and PDFs from the workspace
dataset = workspace.data("data_background_cats")  # Replace "your_dataset_name" with the actual name of your dataset
pdf = workspace.pdf("ProdPDFSumTwoExpPdfchebyshev2_ggh_BDTperyear__cat3")  # Replace "your_pdf_name" with the actual name of your PDF

# Create a frame to plot on
x = workspace.var("mh_ggh")  # Replace "x" with the variable name in your dataset
frame = x.frame()

# Plot the dataset
dataset.plotOn(frame)

# Plot the PDF
pdf.plotOn(frame)

# Create a canvas
canvas = ROOT.TCanvas("canvas", "Dataset and PDF Plot", 800, 600)

# Draw the frame
frame.Draw()

# Add legend or other customizations if needed

# Show the canvas
canvas.Draw()
canvas.SaveAs("testplot.png")
# Close the ROOT file
file.Close()

# Run the event loop

