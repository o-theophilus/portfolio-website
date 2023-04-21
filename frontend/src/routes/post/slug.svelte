<script>
	import { api_url, module, _tick, _user } from '$lib/store.js';

	import Content from '$lib/content.svelte';
	import Marked from '$lib/marked.svelte';
	import Meta from '$lib/meta.svelte';
	import Button from '$lib/button.svelte';
	import Tags from '$lib/tags.svelte';

	import Delete from './slug__delete__.svelte';
	import Title from './slug__edit_title__.svelte';
	import Description from './slug__edit_description__.svelte';
	import Edit_Tags from './slug__edit_tags__.svelte';
	import Edit_Content from './slug__edit_content__.svelte';
	import Edit_Date from './slug__edit_date__.svelte';
	import Edit_Status from './slug__edit_status__.svelte';
	import Manage_Photo from './slug__manage_photo__.svelte';
	import Manage_Video from './slug__manage_video__.svelte';
	import Share from './slug__share__.svelte';
	import Rating from './slug__add_rating__.svelte';
	import Comment from './slug.comment.svelte';
	import Author from './slug.author.svelte';

	export let data;
	let { post } = data;
	let { tags } = data;

	$: if ($_tick) {
		post = $_tick;
		$_tick = '';
	}

	let content = post.content;
	$: {
		content = post.content;
		post.photo_count = 1;
		let is_available = content.search(/{#photo}/) >= 0;
		while (is_available) {
			let photo = `![${post.title}](${api_url}/${post.photos[post.photo_count]})`;
			content = content.replace(/{#photo}/, photo);
			is_available = content.search(/{#photo}/) >= 0;
			post.photo_count = post.photo_count + 1;
		}
	}

	$: {
		post.video_count = 0;
		let is_available = content.search(/{#video}/) >= 0;
		while (is_available) {
			let v = `<iframe 
					width="100%" 
					height="500px"
					frameborder="0" 
					src="https://www.youtube.com/embed/${post.videos[post.video_count]}">
				</iframe>
				`;
			content = content.replace(/{#video}/, v);
			is_available = content.search(/{#video}/) >= 0;
			post.video_count = post.video_count + 1;
		}
	}

	let ratings = 0;
	$: {
		ratings = 0;
		for (const i in post.ratings) {
			ratings += post.ratings[i].rating;
		}
	}

	let edit_mode = false;
</script>

<Meta title={post.title} description={post.description} image={post.photos[0]} />

<Content>
	{#if $_user.roles.includes('admin')}
		<Button
			class="tiny"
			on:click={() => {
				edit_mode = !edit_mode;
			}}>Edit Mode: {edit_mode}</Button
		>
		<br />
		<br />
	{/if}
	<img
		src="{api_url}/{post.photos[0] || ''}"
		alt={post.title}
		onerror="this.src='/site/no_photo.png'"
	/>

	{#if $_user.roles.includes('admin') && edit_mode}
		<div class="row">
			<Button
				class="tiny"
				on:click={() => {
					$module = {
						module: Manage_Photo,

						post
					};
				}}>Manage Photo</Button
			>
			{#if post.video_count > 0}
				<Button
					class="tiny"
					on:click={() => {
						$module = {
							module: Manage_Video,
							post
						};
					}}>Manage Video</Button
				>
			{/if}
		</div>
	{/if}

	<br />
	<strong class="big">{post.title}</strong>
	{#if $_user.roles.includes('admin') && edit_mode}
		<Button
			icon="edit"
			class="tiny"
			on:click={() => {
				$module = {
					module: Title,
					post
				};
			}}
		/>
	{/if}

	<br />
	<span class="date">{post.created_at.split('T')[0]}</span>
	{#if $_user.roles.includes('admin') && edit_mode}
		<Button
			icon="edit"
			class="tiny"
			on:click={() => {
				$module = {
					module: Edit_Date,
					post
				};
			}}
		/>
	{/if}

	{#if $_user.roles.includes('admin') && edit_mode}
		<br /><br />
		{post.description}

		<Button
			icon="edit"
			class="tiny"
			on:click={() => {
				$module = {
					module: Description,
					post
				};
			}}
		/>
	{/if}

	<br /><br />
	{#if $_user.roles.includes('admin') && edit_mode}
		<Button
			icon="edit"
			class="tiny"
			on:click={() => {
				$module = {
					module: Edit_Content,
					post
				};
			}}
		/>
	{/if}
	<Marked md={content} />

	<br />

	{#if $_user.roles.includes('admin') && edit_mode}
		<Button
			icon="edit"
			class="tiny"
			on:click={() => {
				$module = {
					module: Edit_Tags,
					post,
					tags_in: tags
				};
			}}
		/>
	{/if}
	<Tags tags={post.tags} />
	<br /><br />
	<Author />

	{#if $_user.roles.includes('admin') && edit_mode}
		<br /> <br />
		Status: <strong> {post.status}</strong>
		<div class="row">
			<Button
				on:click={() => {
					$module = {
						module: Edit_Status,
						post
					};
				}}>Edit Status</Button
			>
			<Button
				on:click={() => {
					$module = {
						module: Delete,
						post
					};
				}}>Delete</Button
			>
		</div>
	{/if}

	<br /><br />

	{#if $_user.login}
		<Button
			name="Overall Rating: {ratings}"
			icon="heart"
			on:click={() => {
				$module = {
					module: Rating,
					post
				};
			}}
		/>
	{/if}

	<Button
		name="share"
		icon="share"
		on:click={() => {
			$module = {
				module: Share,
				post
			};
		}}
	/>
	<br /><br /><br />
</Content>

<Comment {post} />
<br /><br />

<style>
	.big {
		font-size: x-large;
		color: var(--accent1);
	}
	img {
		background-color: var(--accent4);
	}
</style>
