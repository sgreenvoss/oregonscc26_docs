Here is what I did:

First, I downloaded the latest version of ParaView and unzipped it.

After that, I tried to download ParaView on the interactive desktop (the Bastion node). However, because I kept getting disconnected and didn't know the password to use sudo to install the missing graphic libraries, I changed my approach.

Note: If you clicked on Desktop via Resources, it will direct you into GPU node and report connection problem. I’m not sure if we can do interactive desktop on GPU node or not, but you can return Home and choose Bastion node. However, the folders from GPU node is not shared with Bastion node.

(Disclaimer: Beyond this point, I used AI to help me, so I will try to explain what I understood.)

Fortunately, there is another way: by connecting our laptop directly to the server, we can run ./pvserver on the GPU node to let the remote GPU handle all the heavy graphics rendering and stream the results to our laptop.

The first thing I did was download ParaView on my local laptop.

After adding my SSH key to the server via SSH Setup, they provided connection examples. I'm not sure if everyone's is similar, but mine looked like this:

 <img width="244" height="66" alt="image" src="https://github.com/user-attachments/assets/ccb2bd1a-36a8-4d93-a38e-4d4e79c64412" />

ssh -p 11538 nvidia@global.prd.ga.launchpad.nvidia.com

ssh ssh://nvidia@global.prd.ga.launchpad.nvidia.com:11538

Using the server IP information from those lines, I ran the SSH command in a new command prompt to access the server.

Once inside, I navigated to the directory by running cd Applications/ParaView/bin/ and started the server with ./pvserver. This provided a connection URL.

 <img width="945" height="105" alt="image" src="https://github.com/user-attachments/assets/367b5746-a636-45b7-a59b-00e34026f2db" />

Next, using the server details, I ran a command to link my local port 11111 to the scc-connect-24-gpu01:11111 port on the server: 

ssh -p 11538 -L 11111:scc-connect-24-gpu01:11111 nvidia@global.prd.ga.launchpad.nvidia.com

After completing these steps, my laptop was successfully bridged to the GPU node. The final step was to open ParaView on my laptop, click File, and select Connect at the bottom.

 <img width="372" height="701" alt="image" src="https://github.com/user-attachments/assets/ebbfffdf-920e-46f9-959b-25997f71dc47" />

From there, I added a new server using localhost as the host (since our lap is on the same server with GPU node) and established the connection.

 <img width="847" height="642" alt="image" src="https://github.com/user-attachments/assets/d58c63a4-30dd-4287-802c-054562d9dab5" />

At this point, you should see your files ready to go in the directory.
 <img width="945" height="279" alt="image" src="https://github.com/user-attachments/assets/949c8267-eba3-4248-8b9a-bae593c25d07" />

