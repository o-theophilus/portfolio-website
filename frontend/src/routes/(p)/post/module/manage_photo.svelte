<script>
	import { api_url, loading, tick } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/comp/button.svelte';

	export let post;

	let init_order = [...post.photos];

	let order_changed = false;
	let show_left_btn = true;
	let show_right_btn = true;

	let input;
	let files = [];
	let excess_files = [];
	let invalid_files = [];

	let dragover = false;
	let error = '';

	const make_active = (photo = '', clear_error = true) => {
		if (clear_error) {
			error = '';
		}
		show_left_btn = true;
		show_right_btn = true;
		post.active_photo = photo || post.photos[0] || '';
		let i = post.photos.indexOf(post.active_photo);
		if (i == post.photos.length - 1) {
			show_right_btn = false;
		} else if (i == 0) {
			show_left_btn = false;
		}
	};

	const compare_order = () => {
		order_changed = false;
		for (let i in post.photos) {
			if (init_order[i] != post.photos[i]) {
				order_changed = true;
				break;
			}
		}
	};

	const order_right = () => {
		let index = post.photos.indexOf(post.active_photo);
		if (index < post.photos.length - 1) {
			post.photos.splice(index, 1);
			post.photos.splice(index + 1, 0, post.active_photo);

			post = post;
			make_active(post.active_photo);
			compare_order();
		}
	};

	const order_left = () => {
		let index = post.photos.indexOf(post.active_photo);
		if (index > 0) {
			post.photos.splice(index, 1);
			post.photos.splice(index - 1, 0, post.active_photo);

			post = post;
			make_active(post.active_photo);
			compare_order();
		}
	};

	const reorder_delete = async (method) => {
		error = '';
		$loading = true;
		const resp = await fetch(`${api_url}/${post.type}/photo/${post.slug}`, {
			method: method,
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(post)
		});
		$loading = false;

		if (resp.ok) {
			let data = await resp.json();

			if (data.status == 200) {
				let temp = post.active_photo;
				let temp2 = post.photo_count;
				post = data.data.post;
				post.active_photo = temp;
				post.photo_count = temp2;

				tick(post);

				if (method == 'delete') {
					post.active_photo = post.photos[0] || '';
				}

				init_order = [...post.photos];
				order_changed = false;
			} else {
				error = data.message;
			}
		}
	};

	const on_input = () => {
		files = [];
		excess_files = [];
		invalid_files = [];
		error = '';

		for (let i = 0; i < input.files.length; i++) {
			let file = input.files[i];
			let [media, type] = file.type.split('/');
			if (media == 'image' && !['svg+xml', 'x-icon'].includes(type)) {
				if (files.length < post.photo_count - post.photos.length) {
					files.push(file);
				} else {
					excess_files.push(file.name);
				}
			} else {
				invalid_files.push(file.name);
			}
		}

		files.length > 0 && upload_input();

		if (excess_files.length > 0) {
			error = `
			<strong>
				Excess File${excess_files.length > 1 ? 's' : ''}:
			</strong>
			<br/>
			${excess_files.join(', ')}`;
		}
		if (invalid_files.length > 0) {
			error = `${excess_files.length > 0 ? `${error}<br/><br/>` : ''}

			<strong>
				Invalid File${invalid_files.length > 1 ? 's' : ''}:
			</strong>
			<br/>
			${invalid_files.join(', ')}`;
		}
	};

	const upload_input = async () => {
		let formData = new FormData();
		formData.append('slug', post.slug);
		for (let i in files) {
			formData.append('files', files[i]);
		}

		$loading = true;
		const resp = await fetch(`${api_url}/${post.type}/photo_many/${post.slug}`, {
			method: 'post',
			headers: {
				Authorization: $token
			},
			body: formData
		});
		$loading = false;

		if (resp.ok) {
			let data = await resp.json();

			if (data.status == 200) {
				let temp = post.active_photo;
				let temp2 = post.photo_count;
				post = data.data.post;
				post.active_photo = temp;
				post.photo_count = temp2;

				make_active((clear_error = false));
				tick(post);
			} else {
				error = data.message;
			}
		}
	};

	make_active();
</script>

<section>
	<strong class="big"> Manage Photo </strong>
	<div class="content">
		<img
			class:dragover
			src="{api_url}/{post.active_photo}"
			alt={post.title}
			onerror="this.src='/site/no_photo.png'"
			on:dragover|preventDefault={() => {
				dragover = true;
			}}
			on:dragleave|preventDefault={() => {
				dragover = false;
			}}
			on:drop|preventDefault={(e) => {
				dragover = false;
				input.files = e.dataTransfer.files;
				on_input();
			}}
		/>
		<input
			style:display="none"
			type="file"
			accept="image/*"
			multiple
			bind:this={input}
			on:change={(e) => {
				on_input();
			}}
		/>
		<br />
		{#if post.photos.length > 1}
			<div class="slide">
				{#each post.photos as photo}
					<img
						src="{api_url}/{photo}"
						alt={post.name}
						class:active={post.active_photo == photo}
						on:click={() => {
							make_active(photo);
						}}
						on:keypress
						onerror="this.src='/site/no_photo.png'"
					/>
				{/each}
			</div>
		{/if}

		{#if error}
			<span class="error">
				{@html error}
			</span>
		{/if}

		{#if post.photos.length > 1}
			<br />
			<div class="row">
				{#if show_left_btn}
					<Button
						name="<<"
						on:click={() => {
							order_left();
						}}
					/>
				{/if}
				{#if show_right_btn}
					<Button
						name=">>"
						on:click={() => {
							order_right();
						}}
					/>
				{/if}
				{#if order_changed}
					<Button
						name="Save Order"
						on:click={() => {
							reorder_delete('put');
						}}
					/>
				{/if}
			</div>
		{/if}
		<br />
		<div class="row">
			{#if post.photos.length < post.photo_count}
				<Button
					name="Add ({post.photo_count - post.photos.length})"
					class="primary"
					on:click={() => {
						input.click();
					}}
				/>
			{/if}

			{#if post.photos.length > 0}
				<Button
					name="Remove {post.photos.length > post.photo_count
						? `(${post.photos.length - post.photo_count} excess)`
						: ''}"
					on:click={() => {
						reorder_delete('delete');
					}}
				/>
			{/if}
		</div>
	</div>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;

		width: 100%;
	}
	strong,
	.content {
		padding: var(--gap3);
	}
	strong {
		border-bottom: 2px solid var(--accent3);
	}

	.slide {
		display: flex;
		justify-content: center;
		gap: var(--gap1);
		flex-wrap: wrap;

		/* border: 2px solid var(--accent5); */
		/* padding: var(--gap3); */
	}
	.slide > * {
		display: flex;
		align-items: center;
		justify-content: center;

		--size: 50px;
		width: var(--size);
		height: var(--size);
		cursor: pointer;

		border: 2px solid var(--accent5);
		border-radius: var(--brad1);

		transition: var(--trans1);
	}
	.slide > *:hover {
		border-color: var(--midtone);
		transform: scale(1.1);
	}
	.slide > *.active {
		border-color: var(--color1);
	}
	img {
		border: 2px solid transparent;
	}
	.dragover {
		border-color: var(--color1);
	}
</style>
