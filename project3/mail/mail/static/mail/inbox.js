document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', sendmail)

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {  

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#goininemail').style.display = 'none';


  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#goininemail').style.display = 'none';


  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
        emails.forEach( email => {
        
        console.log(email);

        
        newemail = document.createElement('div')
        newemail.innerHTML = `

            <div class="border">
              <h5>From: ${email.sender}</h5>
              <h5>Subject: ${email.subject}</h5>
              <h5>Date: ${email.timestamp}</h5>
              <button>Learn More</button>
            </div>
        `


        newemail.className = email.read? 'read':'unread'
        newemail.addEventListener('click', function(){
          goinemail(email.id)

        });
        document.querySelector('#emails-view').append(newemail);


      })

      // ... do something else with emails ...
  });
}


function sendmail(event){
  event.preventDefault();
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;
  
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
  });



}








function goinemail(id){
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {

      console.log(email);
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'none';
      document.querySelector('#goininemail').style.display = 'block';

      document.querySelector('#goininemail').innerHTML = `

        <ul class="list-group">
          <li class="list-group-item">From: ${email.sender}</li>
          <li class="list-group-item">To: ${email.recipients}</li>
          <li class="list-group-item">Subject: ${email.subject}</li>
          <li class="list-group-item">Timestamp: ${email.timestamp}</li>
          <li class="list-group-item">Body: ${email.body}</li>

        </ul>





      `


      if( !email.read){
        fetch(`/emails/${email.id}`, {
          method: 'PUT',
          body: JSON.stringify({
              read: true
          })
        })


      }

      const archivebutton = document.createElement('button');
      archivebutton.innerHTML = email.archived ? "Remove Email From Archive" : "Add Email To Archive"
      archivebutton.addEventListener('click', function() {
          
        fetch(`/emails/${email.id}`, {
          method: 'PUT',
          body: JSON.stringify({
              archived: !email.archived   
          })
        })
        .then(() => {load_mailbox('archive')})

      });
      document.querySelector('#goininemail').append(archivebutton);


      const replybutton = document.createElement('button');
      replybutton.innerHTML = "Reply"
      replybutton.addEventListener('click', function() {
          compose_email();

          document.querySelector('#compose-recipients').value = email.sender;
          let subject = email.subject;
          if (subject.split('',1)[0] != "Re:"){
            subject = "Re: " + email.subject;

          }



          document.querySelector('#compose-subject').value = subject;
          document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} Wrote: ${email.body}`;

      });
      document.querySelector('#goininemail').append(replybutton);




  });
}