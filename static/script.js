document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('fetch-data').addEventListener('click', async () => {
      const studentId = document.getElementById('student-id').value;

      if (!studentId) {
          alert('Please enter a Student ID.');
          return;
      }

      try {
          const response = await fetch(`/api/get_growth_rates?stud_id=${studentId}`);
          const data = await response.json();

          if (response.status === 404) {
              alert(data.error);
              return;
          }

          document.getElementById('output-section').style.display = 'block';
          document.getElementById('interests').innerText = data.interests;

          const subjects = Object.keys(data.growth_rates);
          const growthRates = Object.values(data.growth_rates);

          const ctx = document.getElementById('growthChart').getContext('2d');
          new Chart(ctx, {
              type: 'bar',
              data: {
                  labels: subjects,
                  datasets: [{
                      label: 'Growth Rates',
                      data: growthRates,
                      backgroundColor: 'rgba(75, 192, 192, 0.2)',
                      borderColor: 'rgba(75, 192, 192, 1)',
                      borderWidth: 1
                  }]
              },
              options: {
                  scales: {
                      y: {
                          beginAtZero: true
                      }
                  }
              }
          });

      } catch (error) {
          console.error('Error fetching data:', error);
          alert('An error occurred while fetching data.');
      }
  });
});
