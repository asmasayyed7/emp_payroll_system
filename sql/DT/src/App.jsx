import React from "react"
import Particles from "./Particles"



const App = () => {
  return (
    <>
    <div className="w-full h-screen relative bg-black flex justify-center items-center ">

      <div style={{ width: '100%', height: '600px', position: 'relative' }}>
        <Particles
        
          particleColors={["#ffffff"]}
          particleCount={200}
          particleSpread={10}
          speed={0.1}
          particleBaseSize={100}
          moveParticlesOnHover
          alphaParticles={false}
          disableRotation={false}
          pixelRatio={1}
        />
      </div>

      <div className="absolute flex flex-col justify-center items-center">
       <h1 className="text-white font-bold text-5xl mb-4">This is password management system</h1>
       <button className="bg-blue-300 hover:bg-amber-100 cursor-pointer text-white px-4 py-2 rounded-lg"> Login </button>
      </div>
      </div>
    </>
  )
}

export default App