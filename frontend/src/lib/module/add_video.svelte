<script>
	import { api_url, module, tick } from '$lib/store.js';

	import Button from '$lib/comp/button.svelte';
	import Photo_Man from '$lib/module/manage_photo.svelte';

	export let data;
	let { post } = data;
	let { post_type } = data;

	let input;
	let file;

	let default_img = '/site/select_photo.png';
	let src = default_img;
	let error = '';

	const on_change = () => {
		error = '';
		file = input.files[0];
		input.value = null;

		let name = file.name.split('.');
		let ext = name[name.length - 1];

		console.log(name);
		console.log(ext);

		// if (!['jpg', 'png', 'gif'].includes(ext.toLowerCase())) {
		// 	src = default_img;
		// 	error = 'invalid file type';
		// } else {
		// 	let reader = new FileReader();
		// 	reader.readAsDataURL(file);
		// 	reader.onload = (e) => {
		// 		src = e.target.result;
		// 	};
		// }
	};

	const validate = () => {
		if (!file) {
			error = 'please select a photo';
		}
		!error && submit();
	};

	const submit = async () => {
		let formData = new FormData();
		formData.append('photo', file);
		formData.append('slug', post.slug);

		const resp = await fetch(`${api_url}/${post_type}/photo/${post.slug}`, {
			method: 'post',
			headers: {
				// Authorization: $token
			},
			body: formData
		});

		if (resp.ok) {
			let data = await resp.json();
			post = data.data.post;

			if (data.status == 200) {
				tick(post);

				$module = {
					module: Photo_Man,
					data: {
						post,
						post_type
					}
				};
			} else {
				error = data.message;
			}
		}
	};
</script>

<section>
	<strong class="big">
		Add Photo
	</strong>
	<form on:submit|preventDefault novalidate autocomplete="off">
		<img
			{src}
			alt={post.title}
			on:click={() => {
				input.click();
			}}
			on:keypress
		/>
		<input
			type="file"
			accept="video/*"
			bind:this={input}
			on:change={on_change}
			id="img_input"
		/>

		{#if error}
			<div class="inputGroup">
				<span class="error">
					{error}
				</span>
			</div>
		{/if}

		<Button
			class="primary"
			name="Upload"
			on:click={() => {
				validate();
			}}
		/>
	</form>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;

		width: 100%;
	}
	strong,
	form {
		padding: var(--gap3);
	}
	strong {
		border-bottom: 2px solid var(--mid_color);
	}

	img {
		cursor: pointer;
		background-color: var(--foreground);
	}

	#img_input {
		display: none;
	}
</style>
