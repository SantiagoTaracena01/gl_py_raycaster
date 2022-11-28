"""
Universidad del Valle de Guatemala
(CC2018) Gráficos por Computadora
Proyecto 03: Raycaster
Santiago Taracena Puga (20017)
"""

# Código del vertex shader del visor.
vertex_shader = """
  #version 460
  layout (location = 0) in vec3 position;
  layout (location = 1) in vec3 vertexColor;
  uniform mat4 myMatrix;
  out vec3 ourColor;
  void main() {
    gl_Position = myMatrix * vec4(position, 1.0f);
    ourColor = vertexColor;
  }
"""

# Código del fragment shader del visor.
fragment_shader = """
  #version 460
  layout (location = 0) out vec4 fragColor;
  uniform vec3 color;
  in vec3 ourColor;
  void main() {
    fragColor = vec4(color, 1.0f);
  }
"""

fire_shader = """
  #version 460
  const int _VolumeSteps = 128;
  const float _StepSize = 0.02; 
  const float _Density = 0.2;

  const float _SphereRadius = 1.0;
  const float _NoiseFreq = 2.0;
  const float _NoiseAmp = 1.0;
  const vec3 _NoiseAnim = vec3(0, -1, 0);

  float noise(in vec3 x) {
    vec3 p = floor(x);
    vec3 f = fract(x);
    f = f*f*(3.0-2.0*f);
    
    vec2 uv = (p.xy+vec2(37.0,17.0)*p.z) + f.xy;
    vec2 rg = texture( iChannel0, (uv+0.5)/256.0, -100.0 ).yx;
    return mix( rg.x, rg.y, f.z )*2.0-1.0;
  }

  float fbm( vec3 p )
  {
      float f = 0.0;
      float amp = 0.5;
      for(int i=0; i<4; i++)
      {
          //f += abs(noise(p)) * amp;
          f += noise(p) * amp;
          p *= 2.03;
          amp *= 0.5;
    }
      return f;
  }

  vec2 rotate(vec2 v, float angle)
  {
      return v * mat2(cos(angle),sin(angle),-sin(angle),cos(angle));
  }

  // returns signed distance to surface
  float distanceFunc(vec3 p)
  {	

    // distance to sphere
      float d = length(p) - _SphereRadius;
    // offset distance with noise
    d += fbm(p*_NoiseFreq + _NoiseAnim*iTime) * _NoiseAmp;
    return d;
  }

  // shade a point based on distance
  vec4 shade(float d)
  {	
      if (d >= 0.0 && d < 0.2) return (mix(vec4(3, 3, 3, 1), vec4(1, 1, 0, 1), d / 0.2));
    if (d >= 0.2 && d < 0.4) return (mix(vec4(1, 1, 0, 1), vec4(1, 0, 0, 1), (d - 0.2) / 0.2));
    if (d >= 0.4 && d < 0.6) return (mix(vec4(1, 0, 0, 1), vec4(0, 0, 0, 0), (d - 0.4) / 0.2));    
      if (d >= 0.6 && d < 0.8) return (mix(vec4(0, 0, 0, 0), vec4(0, .5, 1, 0.2), (d - 0.6) / 0.2));
      if (d >= 0.8 && d < 1.0) return (mix(vec4(0, .5, 1, .2), vec4(0, 0, 0, 0), (d - 0.8) / 0.2));            
      return vec4(0.0, 0.0, 0.0, 0.0);
  }

  // procedural volume
  // maps position to color
  vec4 volumeFunc(vec3 p)
  {
      //p.xz = rotate(p.xz, p.y*2.0 + iTime);	// firestorm
    float d = distanceFunc(p);
    return shade(d);
  }

  // ray march volume from front to back
  // returns color
  vec4 rayMarch(vec3 rayOrigin, vec3 rayStep, out vec3 pos)
  {
    vec4 sum = vec4(0, 0, 0, 0);
    pos = rayOrigin;
    for(int i=0; i<_VolumeSteps; i++) {
      vec4 col = volumeFunc(pos);
      col.a *= _Density;
      // pre-multiply alpha
      col.rgb *= col.a;
      sum = sum + col*(1.0 - sum.a);	
      pos += rayStep;
    }
    return sum;
  }

  void mainImage( out vec4 fragColor, in vec2 fragCoord )
  {
      vec2 p = (fragCoord.xy / iResolution.xy)*2.0-1.0;
      p.x *= iResolution.x/ iResolution.y;
    
      float rotx = (iMouse.y / iResolution.y)*4.0;
      float roty = -(iMouse.x / iResolution.x)*4.0;

      float zoom = 4.0;

      // camera
      vec3 ro = zoom*normalize(vec3(cos(roty), cos(rotx), sin(roty)));
      vec3 ww = normalize(vec3(0.0,0.0,0.0) - ro);
      vec3 uu = normalize(cross( vec3(0.0,1.0,0.0), ww ));
      vec3 vv = normalize(cross(ww,uu));
      vec3 rd = normalize( p.x*uu + p.y*vv + 1.5*ww );

      ro += rd*2.0;
    
      // volume render
      vec3 hitPos;
      vec4 col = rayMarch(ro, rd*_StepSize, hitPos);

      fragColor = col;
  }
"""

quasicrystal_shader = """
  #version 460
  #define PI 3.141596

  layout (location = 0) out vec4 fragColor;

  vec3 a = vec3(0.5, 0.5, 0.5);
  vec3 b = vec3(0.5, 0.5, 0.5);
  vec3 c = vec3(1.0, 1.0, 1.0);
  vec3 d = vec3(0.00, 0.33, 0.67);

  // iq color mapper
  vec3 colorMap(float t) {
    return (a + b * cos(2. * PI * (c * t + d)));
  }

  void mainImage(out vec4 o, in vec2 i)
  {
      vec2 uv = i / iResolution.xy;
      uv -= 0.5;
      uv.x *= iResolution.x / iResolution.y;
      
      float r = length(uv);
      float a = atan(uv.y, uv.x);
      
      float ring = 1.5 + 0.8 * sin(PI * 0.25 * iTime);
      
      float kr = 0.5 - 0.5 * cos(7. * PI * r); 
      vec3 kq = 0.5 - 0.5 * sin(ring*vec3(30., 29.3, 28.6) * r - 6.0 * iTime + PI * vec3(-0.05, 0.5, 1.0));
      vec3 c = kr * (0.1 + kq * (1. - 0.5* colorMap(a / PI))) * (0.5 + 0.5 * sin(11.*a + 22.5*r));

      // Output to screen
      o.rgb = mix(vec3(0.0, 0.0, 0.2), c, 0.85);
  }
"""

another_shader = """
  #version 460
  layout (location = 0) out vec4 fragColor;
  const float pi = 3.14159;

  float sigmoid(float x){
    return x/(1.+abs(x));   
  }

  float iter(vec2 p, vec4 a, vec4 wt, vec4 ws, float t, float m, float stereo){
      float wp = .2;
      vec4 phase = vec4(mod(t, wp), mod(t+wp*.25, wp), mod(t+wp*.5, wp), mod(t+wp*.75, wp))/wp;
      float zoom = 1./(1.+.5*(p.x*p.x+p.y*p.y));
      vec4 scale = zoom*pow(vec4(2.), -4.*phase);
      vec4 ms = .5-.5*cos(2.*pi*phase);
      vec4 pan = stereo/scale*(1.-phase)*(1.-phase);
      vec4 v = ms*sin( wt*(t+m) + (m+ws*scale)*((p.x+pan) * cos((t+m)*a) + p.y * sin((t+m)*a)));
      return sigmoid(v.x+v.y+v.z+v.w+m);
  }

  vec3 scene(float gt, vec2 uv, vec4 a0, vec4 wt0, vec4 ws0, float blur){
      //time modulation
      float tm = mod(.0411*gt, 1.);
      tm = sin(2.*pi*tm*tm);
      float t = (.04*gt + .05*tm);
      
      float stereo = 1.*(sigmoid(2.*(sin(1.325*t*cos(.5*t))+sin(-.7*t*sin(.77*t)))));//+sin(-17.*t)+sin(10.*t))));
      //t = 0.;
      //also apply spatial offset
      uv+= .5*sin(.33*t)*vec2(cos(t), sin(t));
      
      //wildly iterate and divide
      float p0 = iter(uv, a0, wt0, ws0, t, 0., stereo);
      
      float p1 = iter(uv, a0, wt0, ws0, t, p0, stereo);
      
      float p2 = sigmoid(p0/(p1+blur));
      
      float p3 = iter(uv, a0, wt0, ws0, t, p2, stereo);
      
      float p4 = sigmoid(p3/(p2+blur));
      
      float p5 = iter(uv, a0, wt0, ws0, t, p4, stereo);
      
      float p6 = sigmoid(p4/(p5+blur));
      
      float p7 = iter(uv, a0, wt0, ws0, t, p6, stereo);
      
      float p8 = sigmoid(p4/(p2+blur));
      
      float p9 = sigmoid(p8/(p7+blur));
      
      float p10 = iter(uv, a0, wt0, ws0, t, p8, stereo);
      
      float p11 = iter(uv, a0, wt0, ws0, t, p9, stereo);
      
      float p12 = sigmoid(p11/(p10+blur));
      
      float p13 = iter(uv, a0, wt0, ws0, t, p12, stereo);
      
      //colors
      vec3 accent_color = vec3(1.,0.2,0.);//vec3(0.99,0.5,0.2);
      /*float r = sigmoid(-1.+2.*p0+p1-max(1.*p3,0.)+p5+p7+p10+p11+p13);
      float g = sigmoid(-1.+2.*p0-max(1.*p1,0.)-max(2.*p3,0.)-max(2.*p5,0.)+p7+p10+p11+p13);
      float b = sigmoid(0.+1.5*p0+p1+p3+-max(2.*p5,0.)+p7+p10+p11+p13);
      */
      float r = sigmoid(p0+p1+p5+p7+p10+p11+p13);
      float g = sigmoid(p0-p1+p3+p7+p10+p11);
      float b = sigmoid(p0+p1+p3+p5+p11+p13);
      
      
      vec3 c = max(vec3(0.), .4+.6*vec3(r,g,b));
      
      float eps = .4;
      float canary = min(abs(p1), abs(p2));
      canary = min(canary, abs(p5));
      //canary = min(canary, abs(p6));
      canary = min(canary, abs(p7));
      canary = min(canary, abs(p10));
      float m = max(0.,eps-canary)/eps;
      m = sigmoid((m-.5)*700./(1.+10.*blur))*.5+.5;
      //m = m*m*m*m*m*m*m*m*m*m;
      vec3 m3 = m*(1.-accent_color);
      c *= .8*(1.-m3)+.3;//mix(c, vec3(0.), m);
      
      return c;
  }

  void mainImage( out vec4 fragColor, in vec2 fragCoord )
  {
      float s = min(iResolution.x, iResolution.y);
      vec2 uv = (2.*fragCoord.xy - vec2(iResolution.xy)) / s;
      
      float blur = .5*(uv.x*uv.x+uv.y*uv.y);
      
      //angular, spatial and temporal frequencies
      vec4 a0 = pi*vec4(.1, -.11, .111, -.1111); 
      vec4 wt0 = 2.*pi*vec4(.3);//.3333, .333, .33, .3);
      vec4 ws0 = 2.5*vec4(11., 13., 11., 5.);

      //aa and motion blur
      float mb = 1.;
      float t = 1100.+iTime;
      vec3 c = scene(t, uv, a0, wt0, ws0, blur)
          + scene(t-mb*.00185, uv+(1.+blur)*vec2(.66/s, 0.), a0, wt0, ws0, blur)
          + scene(t-mb*.00370, uv+(1.+blur)*vec2(-.66/s, 0.), a0, wt0, ws0, blur)
          + scene(t-mb*.00555, uv+(1.+blur)*vec2(0., .66/s), a0, wt0, ws0, blur)
          + scene(t-mb*.00741, uv+(1.+blur)*vec2(0., -.66/s), a0, wt0, ws0, blur)
          + scene(t-mb*.00926, uv+(1.+blur)*vec2(.5/s, .5/s), a0, wt0, ws0, blur)
          + scene(t-mb*.01111, uv+(1.+blur)*vec2(-.5/s, .5/s), a0, wt0, ws0, blur)
          + scene(t-mb*.01296, uv+(1.+blur)*vec2(-.5/s, -.5/s), a0, wt0, ws0, blur)
          + scene(t-mb*.01481, uv+(1.+blur)*vec2(.5/s, -.5/s), a0, wt0, ws0, blur)

          ;
      c/=9.;
      
      fragColor = vec4(c,1.0);
  }
"""
