<script>
	import { api_url, module, tick } from '$lib/store.js';

	import Button from '$lib/comp/button.svelte';
	import Add from './add_photo.svelte';

	export let data;
	let { post } = data;
	let { post_type } = data;

	let init_order = [...post.photos];

	let error = '';
	let order_changed = false;
	let show_left_btn = true;
	let show_right_btn = true;

	const make_active = (photo = '') => {
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

	const submit = async (method) => {
		error = '';
		const resp = await fetch(`${api_url}/${post_type}/photo/${post.slug}`, {
			method: method,
			headers: {
				'Content-Type': 'application/json'
				// Authorization: $token
			},
			body: JSON.stringify(post)
		});

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

	make_active();
</script>

<section>
	<strong class="big">
		Manage {post_type} photo
	</strong>
	<div class="content">
		<img
			src="{api_url}/{post.active_photo}"
			alt={post.title}
			onerror="this.src='/site/no_photo.png'"
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

			{#if error}
				<p class="error">
					{error}
				</p>
			{/if}
			<br />
			<div class="row">
				{#if show_left_btn}
					<Button
						name="Left"
						on:click={() => {
							order_left();
						}}
					/>
				{/if}
				{#if show_right_btn}
					<Button
						name="Right"
						on:click={() => {
							order_right();
						}}
					/>
				{/if}
				{#if order_changed}
					<Button
						name="Save Order"
						on:click={() => {
							submit('put');
						}}
					/>
				{/if}
			</div>
		{/if}
		<br />
		<div class="row">
			{#if post.photos.length <= post.photo_count}
				<Button
					name="Add"
					class="primary"
					on:click={() => {
						$module = {
							module: Add,
							data: {
								post,
								post_type
							}
						};
					}}
				/>
			{/if}

			{#if post.photos.length > 0}
				<Button
					name="Remove"
					on:click={() => {
						submit('delete');
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
		border-bottom: 2px solid var(--mid_color);
	}

	.slide {
		display: flex;
		justify-content: center;
		gap: var(--gap1);
		flex-wrap: wrap;

		/* border: 2px solid var(--background); */
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

		border: 2px solid var(--background);
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
</style>
