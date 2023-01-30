<script>
	import Loader from "$lib/components/Loader.svelte"
	let file;
	let loader = false

	async function handleSubmit(event) {
		loader = true
		event.preventDefault();
		const formData = new FormData();
		formData.append("file", file);
	
		try {
			const response = await fetch("http://127.0.0.1:8000/files/", {
			method: "POST",
			body: formData,
			});
			const data = await response.json();
			loader = false
			console.log(data);
		} catch (error) {
			console.error(error);
		}
	}
  
	function handleFileChange(event) {
		file = event.target.files[0];
	}
  </script>
  
{#if loader==true}
	<Loader/>
{/if}
{#if loader==false}
	<form on:submit={handleSubmit} class="mx-3 mb-10">
	<input type="file" on:change={handleFileChange} class="file-input file-input-bordered w-full max-w-xs" />
	<button class = "btn btn-wide mt-16"type="submit">Upload</button>
	</form>
{/if}
