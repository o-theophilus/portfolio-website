<script>
	import { api_url, module, tick } from '$lib/store.js';

	import Button from '$lib/comp/button.svelte';
	import Photo_Man from '$lib/module/manage_photo.svelte';

	export let post;

	let input;
	let files = [];
	let bad_files = [];
	let error = '';

	const on_change = () => {
		error = '';

		for (let i = 0; i < input.files.length; i++) {
			let file = input.files[i];
			let media_type = input.files[i].type.split('/');
			let temp = {
				file: input.files[i],
				name: file.name,
				media: media_type[0],
				type: media_type[1],
				lastModified: input.files[i].lastModified,
				size: input.files[i].size
			};

			const is_new = () => {
				let a = [...files, ...bad_files];

				for (let j = 0; j < a.length; j++) {
					if (
						a[j].name == temp.name &&
						a[j].media == temp.media &&
						a[j].type == temp.type &&
						a[j].lastModified == temp.lastModified &&
						a[j].size == temp.size
					) {
						return false;
					}
				}

				return true;
			};

			if (is_new()) {
				if (['image', 'video'].includes(temp.media) && !['svg+xml', 'x-icon'].includes(temp.type)) {
					let reader = new FileReader();
					reader.readAsDataURL(input.files[i]);
					reader.onload = () => {
						temp.src = reader.result;
					};
					files.push(temp);
					files = files;
				} else {
					temp.error = 'invalid file';
					bad_files.push(temp);
					bad_files = bad_files;
				}
			}
		}
	};

	const validate = () => {
		error = '';
		if (files.length != 0) {
			submit();
		} else {
			error = 'please select a photo';
		}
	};
	const submit = async () => {
		let formData = new FormData();
		formData.append('slug', post.slug);
		for (let i = 0; i < files.length; i++) {
			formData.append('files', files[i].file);
		}

		const resp = await fetch(`${api_url}/${post.type}/photo_many/${post.slug}`, {
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
					post
				};
			} else {
				bad_files = data.message;
			}
		}
	};

	let active = {
		media: 'image',
		src: '/site/select_photo.png'
	};
	let dragover = false;
</script>

<section>
	<strong class="big"> Add Photo </strong>

	<div class:dragover class="display">
		{#if active.media == 'image'}
			<img
				src={active.src}
				alt={post.title}
				on:click={() => {
					input.click();
				}}
				on:keypress
				on:dragover|preventDefault={() => {
					dragover = true;
				}}
				on:dragleave|preventDefault={() => {
					dragover = false;
				}}
				on:drop|preventDefault={(e) => {
					dragover = false;
					input.files = e.dataTransfer.files;
					on_change();
				}}
			/>
		{:else if active.media == 'video'}
			<video
				controls
				src={active.src}
				on:click={() => {
					input.click();
				}}
				on:keypress
			>
				<track kind="captions" /></video
			>
		{/if}
	</div>

	{#each files as f}
		<Button
			on:click={() => {
				active = f;
			}}
			>{f.name}
		</Button>
	{/each}
	{#each bad_files as e}
		<div>
			<span class="error">
				{e.name} - {e.error} ({e.type})
			</span>
		</div>
	{/each}
	<form on:submit|preventDefault novalidate autocomplete="off">
		<input
			type="file"
			accept="image/*, video/*"
			bind:this={input}
			on:change={on_change}
			id="img_input"
			multiple
		/>
		{#if error}
			<span class="error">
				{error}
			</span>
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

	video,
	img {
		cursor: pointer;
		background-color: var(--foreground);
		width: 100%;
	}

	#img_input {
		display: none;
	}
	.display {
		border: 2px solid transparent;
	}
	.display:hover,
	.dragover {
		border-color: var(--color1);
	}
</style>
