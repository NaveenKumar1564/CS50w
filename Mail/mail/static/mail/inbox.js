document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#view-email').style.display = 'none';


  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // post email

  document.querySelector('#compose-form').onsubmit = () => {

    fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
  })
  load_mailbox('sent');
  return false;
  
}
}



function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#view-email').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // inbox get email
  if (mailbox=="inbox"){
   fetch('/emails/inbox')
   .then(response => response.json())
   .then(emails => {
    // Print emails
    console.log(emails);
    

    emails.forEach(email => {

  
      const div = document.createElement("div")
      div.style.border= "double";

      const button = document.createElement("button")
      button.innerHTML = "Archieve"

      if (email.read){
        div.style.backgroundColor = "gray";
      }
      else{
        div.style.backgroundColor = "white";
      }

      div.innerHTML =

      `<div>  ${email.sender} | ${email.subject} | ${email.timestamp} |  </div>`;
    

     document.querySelector("#emails-view").append(div) 
     document.querySelector("#emails-view").append(button) 
  
     button.addEventListener('click', function (){

      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: true
        })
      })    
    })

   
      div.addEventListener('click', function() {


        document.querySelector('#emails-view').style.display = 'none';
        document.querySelector('#compose-view').style.display = 'none';
        document.querySelector('#view-email').style.display = 'block';
      
          fetch(`/emails/${email.id}`)
          .then(response => response.json())
          .then(email => {
          // Print email
          console.log(email);

          const view_email = document.querySelector("#view-email");

          const Reply = document.createElement("button")
          Reply.innerHTML = ("Reply")

          view_email.innerHTML = `

    
          <div>Sender: ${email.sender}</div>
          <div>Recipient: ${email.recipients}</div>
          <div>Subject: ${email.subject}</div>
          <div>Timestamp: ${email.timestamp}</div>
      
          `;

          const hr = document.createElement("hr");
          view_email.append(hr)

          const body2 = document.createElement("div");
          body2.textContent = email.body
          view_email.append(body2)
          view_email.append(Reply)


         Reply.addEventListener('click', function(){


          document.querySelector('#emails-view').style.display = 'none';
          document.querySelector('#compose-view').style.display = 'block';
          document.querySelector('#view-email').style.display = 'none';

           document.querySelector('#compose-recipients').value = email.sender;

           if (email.subject.indexOf("Re: ")=== -1){
            document.querySelector('#compose-subject').value = "Re: "+email.subject;
           }

           document.querySelector('#compose-body').value = ` On ${email.timestamp}| ${email.sender} "wrote:  ${email.body}" Reply: `;


           document.querySelector('#compose-form').onsubmit = () => {

            fetch('/emails', {
            method: 'POST',
            body: JSON.stringify({
                recipients: document.querySelector('#compose-recipients').value,
                subject: document.querySelector('#compose-subject').value,
                body: document.querySelector('#compose-body').value
            })
          });
        }

         })


          fetch(`/emails/${email.id}`,{
             method: 'PUT',
             body: JSON.stringify({
             read: true

          })

          });
    
    });
      
      })

    
  
  })})}

  else if(mailbox=="sent")
  {
    fetch('/emails/sent')
   .then(response => response.json())
   .then(emails => {
    // Print emails
    console.log(emails);
       
    emails.forEach(email => {

  
        const div = document.createElement("div")
        div.style.border= "double";


        div.innerHTML =

      `<div>  ${email.sender} | ${email.subject} | ${email.timestamp} </div>`;

      document.querySelector("#emails-view").append(div) 


      div.addEventListener('click', function() {


        document.querySelector('#emails-view').style.display = 'none';
        document.querySelector('#compose-view').style.display = 'none';
        document.querySelector('#view-email').style.display = 'block';
      
          fetch(`/emails/${email.id}`)
          .then(response => response.json())
          .then(email => {
          // Print email
          console.log(email);

        const view_email = document.querySelector("#view-email");

          view_email.innerHTML = `

    
          <div>Sender: ${email.sender}</div>
          <div>Recipient: ${email.recipients}</div>
          <div>Subject: ${email.subject}</div>
          <div>Timestamp: ${email.timestamp}</div>
        
          `;

          const hr = document.createElement("hr");
          view_email.append(hr)

          const body2 = document.createElement("div");
          body2.textContent = email.body
          view_email.append(body2)
    
    })
  })
    })

   })

    
  }
  
  else if(mailbox=="archive")
  {
    fetch('/emails/archive')
   .then(response => response.json())
   .then(emails => {
    // Print emails
    console.log(emails);
   // load_mailbox("archive");

    emails.forEach(email => {

  
      const div = document.createElement("div")
      div.style.border= "double";


      div.innerHTML =

    `<div>  ${email.sender} | ${email.subject} | ${email.timestamp} </div>`;

    document.querySelector("#emails-view").append(div) 


    div.addEventListener('click', function() {


      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'none';
      document.querySelector('#view-email').style.display = 'block';
    
        fetch(`/emails/${email.id}`)
        .then(response => response.json())
        .then(email => {
        // Print email
        console.log(email);


        const view_email = document.querySelector("#view-email");

          const Unarchive = document.createElement("button")
          Unarchive.innerHTML = ("Unarchive")

          view_email.innerHTML = `

    
          <div>Sender: ${email.sender}</div>
          <div>Recipient: ${email.recipients}</div>
          <div>Subject: ${email.subject}</div>
          <div>Timestamp: ${email.timestamp}</div>
     
          `;

          const hr = document.createElement("hr");
          view_email.append(hr)

          const body2 = document.createElement("div");
          body2.textContent = email.body
          view_email.append(body2)
   
          view_email.append(Unarchive)


      Unarchive.addEventListener('click', function(){

        fetch(`/emails/${email.id}`, {
          method: 'PUT',
          body: JSON.stringify({
              archived: false
          })
        })
        load_mailbox("inbox")


      });
        });
  });
});

 });
};

}
