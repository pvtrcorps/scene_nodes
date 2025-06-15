import bpy
from .base import BaseNode, build_props_and_sockets


class CyclesRenderNode(BaseNode):
    bl_idname = "CyclesRenderNodeType"
    bl_label = "Cycles Render Properties"

    def init(self, context):
        self.inputs.new('SceneSocketType', "Scene")
        self.add_property_sockets()
        self.outputs.new('SceneSocketType', "Scene")

    def draw_buttons(self, context, layout):
        current_cat = None
        for attr, label, _socket, category in self.__class__._prop_defs:
            if category and category != current_cat:
                layout.label(text=category)
                current_cat = category
            layout.prop(self, attr, text=label)


build_props_and_sockets(
    CyclesRenderNode,
    [
        ("logLevel", "int", {"name": "Log Level", "default": 0}, "General"),
        ("device", "string", {"name": "Device"}, "General"),
        ("shadingSystem", "enum", {"name": "Shading System", "items": [("OSL", "OSL", ""), ("SVM", "SVM", "")]}, "General"),
        ("samples", "int", {"name": "Samples", "default": 128}, "Sampling"),
        ("pixelSize", "int", {"name": "Pixel Size", "default": 1}, "Sampling"),
        ("numThreads", "int", {"name": "Threads", "default": 0}, "Performance"),
        ("timeLimit", "float", {"name": "Time Limit", "default": 0.0}, "Performance"),
        ("useProfiling", "bool", {"name": "Use Profiling", "default": False}, "Performance"),
        ("useAutoTile", "bool", {"name": "Use Auto Tile", "default": False}, "Performance"),
        ("tileSize", "int", {"name": "Tile Size", "default": 64}, "Performance"),
        ("bvhLayout", "int", {"name": "BVH Layout", "default": 8}, "Acceleration"),
        ("useBvhSpatialSplit", "bool", {"name": "BVH Spatial Split", "default": False}, "Acceleration"),
        ("useBvhUnalignedNodes", "bool", {"name": "BVH Unaligned Nodes", "default": False}, "Acceleration"),
        ("numBvhTimeSteps", "int", {"name": "BVH Time Steps", "default": 0}, "Acceleration"),
        ("hairSubdivisions", "int", {"name": "Hair Subdivisions", "default": 0}, "Hair"),
        ("hairShape", "enum", {"name": "Hair Shape", "items": [("RIBBONS", "Rounded Ribbons", ""), ("3D", "3D Curves", "")]}, "Hair"),
        ("textureLimit", "int", {"name": "Texture Limit", "default": 0}, "Textures"),
        ("minBounce", "int", {"name": "Min Bounce", "default": 0}, "Light Paths"),
        ("maxBounce", "int", {"name": "Max Bounce", "default": 7}, "Light Paths"),
        ("maxDiffuseBounce", "int", {"name": "Max Diffuse Bounce", "default": 7}, "Light Paths"),
        ("maxGlossyBounce", "int", {"name": "Max Glossy Bounce", "default": 7}, "Light Paths"),
        ("maxTransmissionBounce", "int", {"name": "Max Transmission Bounce", "default": 7}, "Light Paths"),
        ("maxVolumeBounce", "int", {"name": "Max Volume Bounce", "default": 7}, "Light Paths"),
        ("transparentMinBounce", "int", {"name": "Transparent Min Bounce", "default": 0}, "Light Paths"),
        ("transparentMaxBounce", "int", {"name": "Transparent Max Bounce", "default": 7}, "Light Paths"),
        ("aoBounces", "int", {"name": "AO Bounces", "default": 0}, "Light Paths"),
        ("aoFactor", "float", {"name": "AO Factor", "default": 1.0}, "Light Paths"),
        ("aoDistance", "float", {"name": "AO Distance", "default": 0.0}, "Light Paths"),
        ("volumeMaxSteps", "int", {"name": "Volume Max Steps", "default": 1024}, "Volumes"),
        ("volumeStepRate", "float", {"name": "Volume Step Rate", "default": 1.0}, "Volumes"),
        ("causticsReflective", "bool", {"name": "Reflective Caustics", "default": True}, "Caustics"),
        ("causticsRefractive", "bool", {"name": "Refractive Caustics", "default": True}, "Caustics"),
        ("filterGlossy", "float", {"name": "Filter Glossy", "default": 0.0}, "Sampling"),
        ("useFrameAsSeed", "bool", {"name": "Use Frame As Seed", "default": True}, "Sampling"),
        ("seed", "int", {"name": "Seed", "default": 0}, "Sampling"),
        ("sampleClampDirect", "float", {"name": "Clamp Direct", "default": 0.0}, "Sampling"),
        ("sampleClampIndirect", "float", {"name": "Clamp Indirect", "default": 0.0}, "Sampling"),
        ("startSample", "int", {"name": "Start Sample", "default": 0}, "Sampling"),
        ("useLightTree", "bool", {"name": "Use Light Tree", "default": True}, "Lighting"),
        ("lightSamplingThreshold", "float", {"name": "Light Sampling Threshold", "default": 0.0}, "Lighting"),
        ("useAdaptiveSampling", "bool", {"name": "Adaptive Sampling", "default": False}, "Adaptive Sampling"),
        ("adaptiveThreshold", "float", {"name": "Adaptive Threshold", "default": 0.0}, "Adaptive Sampling"),
        ("adaptiveMinSamples", "int", {"name": "Adaptive Min Samples", "default": 0}, "Adaptive Sampling"),
        ("samplingPattern", "string", {"name": "Sampling Pattern"}, "Sampling"),
        ("denoiserType", "enum", {"name": "Denoiser Type", "items": [("OPTIX", "OptiX", ""), ("OIDN", "OpenImageDenoise", ""), ("NONE", "None", "")]}, "Denoising"),
        ("denoiseStartSample", "int", {"name": "Denoise Start Sample", "default": 0}, "Denoising"),
        ("useDenoisePassAlbedo", "bool", {"name": "Use Denoise Pass Albedo", "default": True}, "Denoising"),
        ("useDenoisePassNormal", "bool", {"name": "Use Denoise Pass Normal", "default": True}, "Denoising"),
        ("denoiserPrefilter", "enum", {"name": "Denoiser Prefilter", "items": [("NONE", "None", ""), ("FAST", "Fast", ""), ("ACCURATE", "Accurate", "")]}, "Denoising"),
        ("useGuiding", "bool", {"name": "Use Guiding", "default": False}, "Path Guiding"),
        ("useSurfaceGuiding", "bool", {"name": "Surface Guiding", "default": True}, "Path Guiding"),
        ("useVolumeGuiding", "bool", {"name": "Volume Guiding", "default": True}, "Path Guiding"),
        ("guidingTrainingSamples", "int", {"name": "Guiding Training Samples", "default": 0}, "Path Guiding"),
        ("bgUseShader", "bool", {"name": "Use Background Shader", "default": True}, "Background"),
        ("bgCameraVisibility", "bool", {"name": "Background Camera Visibility", "default": True}, "Background"),
        ("bgDiffuseVisibility", "bool", {"name": "Background Diffuse Visibility", "default": True}, "Background"),
        ("bgGlossyVisibility", "bool", {"name": "Background Glossy Visibility", "default": True}, "Background"),
        ("bgTransmissionVisibility", "bool", {"name": "Background Transmission Visibility", "default": True}, "Background"),
        ("bgShadowVisibility", "bool", {"name": "Background Shadow Visibility", "default": True}, "Background"),
        ("bgScatterVisibility", "bool", {"name": "Background Scatter Visibility", "default": True}, "Background"),
        ("bgTransparent", "bool", {"name": "Background Transparent", "default": False}, "Background"),
        ("bgTransparentGlass", "bool", {"name": "Background Transparent Glass", "default": False}, "Background"),
        ("bgTransparentRoughnessThreshold", "float", {"name": "Background Transparent Roughness", "default": 0.0}, "Background"),
        ("volumeStepSize", "float", {"name": "Volume Step Size", "default": 0.0}, "Film"),
        ("exposure", "float", {"name": "Exposure", "default": 1.0}, "Film"),
        ("passAlphaThreshold", "float", {"name": "Pass Alpha Threshold", "default": 0.5}, "Film"),
        ("displayPass", "string", {"name": "Display Pass"}, "Film"),
        ("showActivePixels", "bool", {"name": "Show Active Pixels", "default": False}, "Film"),
        ("filterType", "string", {"name": "Filter Type"}, "Image Filter"),
        ("filterWidth", "float", {"name": "Filter Width", "default": 1.5}, "Image Filter"),
        ("mistStart", "float", {"name": "Mist Start", "default": 5.0}, "Mist"),
        ("mistDepth", "float", {"name": "Mist Depth", "default": 25.0}, "Mist"),
        ("mistFalloff", "string", {"name": "Mist Falloff"}, "Mist"),
        ("cryptomatteAccurate", "bool", {"name": "Cryptomatte Accurate", "default": False}, "Cryptomatte"),
        ("cryptomatteDepth", "int", {"name": "Cryptomatte Depth", "default": 6}, "Cryptomatte"),
        ("dicingCamera", "string", {"name": "Dicing Camera"}, "Subdivision"),
        ("useTextureCache", "bool", {"name": "Use Texture Cache", "default": False}, "Texture Cache"),
        ("textureCacheSize", "int", {"name": "Texture Cache Size", "default": 1024}, "Texture Cache"),
        ("textureAutoConvert", "bool", {"name": "Texture Auto Convert", "default": True}, "Texture Cache"),
        ("textureAcceptUnmipped", "bool", {"name": "Accept Unmipped", "default": True}, "Texture Cache"),
        ("textureAcceptUntiled", "bool", {"name": "Accept Untiled", "default": True}, "Texture Cache"),
        ("textureAutoTile", "bool", {"name": "Texture Auto Tile", "default": False}, "Texture Cache"),
        ("textureAutoMip", "bool", {"name": "Texture Auto Mip", "default": False}, "Texture Cache"),
        ("textureTileSize", "int", {"name": "Texture Tile Size", "default": 64}, "Texture Cache"),
        ("textureBlurDiffuse", "float", {"name": "Texture Blur Diffuse", "default": 0.0}, "Texture Cache"),
        ("textureBlurGlossy", "float", {"name": "Texture Blur Glossy", "default": 0.0}, "Texture Cache"),
        ("useCustomCachePath", "bool", {"name": "Use Custom Cache Path", "default": False}, "Texture Cache"),
        ("customCachePath", "string", {"name": "Custom Cache Path", "subtype": "DIR_PATH"}, "Texture Cache"),
    ],
)
