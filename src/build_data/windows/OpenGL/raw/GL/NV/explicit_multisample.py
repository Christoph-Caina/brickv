'''OpenGL extension NV.explicit_multisample

Automatically generated by the get_gl_extensions script, do not edit!
'''
from OpenGL import platform, constants, constant, arrays
from OpenGL import extensions
from OpenGL.GL import glget
import ctypes
EXTENSION_NAME = 'GL_NV_explicit_multisample'
_DEPRECATED = False
GL_SAMPLE_POSITION_NV = constant.Constant( 'GL_SAMPLE_POSITION_NV', 0x8E50 )
GL_SAMPLE_MASK_NV = constant.Constant( 'GL_SAMPLE_MASK_NV', 0x8E51 )
GL_SAMPLE_MASK_VALUE_NV = constant.Constant( 'GL_SAMPLE_MASK_VALUE_NV', 0x8E52 )
GL_TEXTURE_BINDING_RENDERBUFFER_NV = constant.Constant( 'GL_TEXTURE_BINDING_RENDERBUFFER_NV', 0x8E53 )
glget.addGLGetConstant( GL_TEXTURE_BINDING_RENDERBUFFER_NV, (1,) )
GL_TEXTURE_RENDERBUFFER_DATA_STORE_BINDING_NV = constant.Constant( 'GL_TEXTURE_RENDERBUFFER_DATA_STORE_BINDING_NV', 0x8E54 )
glget.addGLGetConstant( GL_TEXTURE_RENDERBUFFER_DATA_STORE_BINDING_NV, (1,) )
GL_TEXTURE_RENDERBUFFER_NV = constant.Constant( 'GL_TEXTURE_RENDERBUFFER_NV', 0x8E55 )
GL_SAMPLER_RENDERBUFFER_NV = constant.Constant( 'GL_SAMPLER_RENDERBUFFER_NV', 0x8E56 )
GL_INT_SAMPLER_RENDERBUFFER_NV = constant.Constant( 'GL_INT_SAMPLER_RENDERBUFFER_NV', 0x8E57 )
GL_UNSIGNED_INT_SAMPLER_RENDERBUFFER_NV = constant.Constant( 'GL_UNSIGNED_INT_SAMPLER_RENDERBUFFER_NV', 0x8E58 )
GL_MAX_SAMPLE_MASK_WORDS_NV = constant.Constant( 'GL_MAX_SAMPLE_MASK_WORDS_NV', 0x8E59 )
glget.addGLGetConstant( GL_MAX_SAMPLE_MASK_WORDS_NV, (1,) )
glGetMultisamplefvNV = platform.createExtensionFunction( 
'glGetMultisamplefvNV',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLenum,constants.GLuint,arrays.GLfloatArray,),
doc='glGetMultisamplefvNV(GLenum(pname), GLuint(index), GLfloatArray(val)) -> None',
argNames=('pname','index','val',),
deprecated=_DEPRECATED,
)

glSampleMaskIndexedNV = platform.createExtensionFunction( 
'glSampleMaskIndexedNV',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLuint,constants.GLbitfield,),
doc='glSampleMaskIndexedNV(GLuint(index), GLbitfield(mask)) -> None',
argNames=('index','mask',),
deprecated=_DEPRECATED,
)

glTexRenderbufferNV = platform.createExtensionFunction( 
'glTexRenderbufferNV',dll=platform.GL,
extension=EXTENSION_NAME,
resultType=None, 
argTypes=(constants.GLenum,constants.GLuint,),
doc='glTexRenderbufferNV(GLenum(target), GLuint(renderbuffer)) -> None',
argNames=('target','renderbuffer',),
deprecated=_DEPRECATED,
)


def glInitExplicitMultisampleNV():
    '''Return boolean indicating whether this extension is available'''
    return extensions.hasGLExtension( EXTENSION_NAME )
