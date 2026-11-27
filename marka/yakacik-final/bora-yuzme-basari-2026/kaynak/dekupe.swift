import Vision
import CoreImage
import AppKit
let a = CommandLine.arguments
let ci = CIImage(contentsOf: URL(fileURLWithPath: a[1]))!
let req = VNGenerateForegroundInstanceMaskRequest()
let h = VNImageRequestHandler(ciImage: ci)
try h.perform([req])
guard let r = req.results?.first else { print("no subject"); exit(1) }
print("instances:", r.allInstances.count)
var set = IndexSet()
if a.count > 3 { for s in a[3].split(separator: ",") { set.insert(Int(s)!) } } else { set = r.allInstances }
let pb = try r.generateMaskedImage(ofInstances: set, from: h, croppedToInstancesExtent: false)
let out = CIImage(cvPixelBuffer: pb)
let ctx = CIContext()
try ctx.writePNGRepresentation(of: out, to: URL(fileURLWithPath: a[2]), format: .RGBA8, colorSpace: CGColorSpaceCreateDeviceRGB())
